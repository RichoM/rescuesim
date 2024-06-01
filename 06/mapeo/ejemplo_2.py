# Ejemplo 2: Agregamos información extra al mapa y mejoramos la navegación
from controller import Robot
from enum import Enum
import math

TIME_STEP = 32
MAX_VEL = 6.28

# En este archivo vamos a escribir la representación textual del mapa 
# trazado a medida que recorremos el laberinto.
# IMPORTANTE: Cambiar el valor de esta cadena de texto para que apunte
# a una carpeta válida en el sistema (de otra forma, dará error)
FILE = r"X:\RoboCupRescue\temp\map.txt"

# Declaramos las 4 direcciones en las que puede estar "mirando" el robot
class Direction(Enum):
    UP = 0      # Arriba
    RIGHT = 1   # Derecha
    DOWN = 2    # Abajo
    LEFT = 3    # Izquierda

robot = Robot() 

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

# Usaremos los siguientes sensores de distancia
# - ps7 para chequear la pared al frente
# - ps2 para chequear la pared a la derecha
# - ps4 para chequear la pared atrás
# - ps5 para chequear la pared a la izquierda 
ps7 = robot.getDevice("ps7")
ps2 = robot.getDevice("ps2")
ps5 = robot.getDevice("ps5")
ps4 = robot.getDevice("ps4")
ps7.enable(TIME_STEP)
ps2.enable(TIME_STEP)
ps5.enable(TIME_STEP)
ps4.enable(TIME_STEP)

# El giroscopio nos permitirá saber la orientación del robot
gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)

# Y el gps su ubicación en el mapa
gps = robot.getDevice("gps")
gps.enable(TIME_STEP)

position = None
direction = None
rotation = 0.25*math.tau
currentTime = robot.getTime()

# En el siguiente dictionary vamos a registrar las baldosas visitadas,
# Como claves usaremos siempre la columna y fila de cada baldosa, de 
# esta forma podremos armar muy fácilmente una grilla dinámica.
# IMPORTANTE: El formato que espera el supervisor para otorgar puntaje 
# por el trazado del mapa es una matriz, NO un dictionary. Sin embargo,
# vamos a usar un formato más flexible para simplificar el algoritmo.
# Luego será necesario aplicar una función de transformación que genere
# la matriz correcta a partir del dictionary (no incluido en este ejemplo)
grid = {}

# Necesitamos también guardar la posición del robot relativa a la celda
# de origen. En lugar de usar simplemente la variable "position", que 
# representa la posición absoluta en metros, declaramos dos variables
# "row" y "col", que representan índices dentro de la grilla
row = 0
col = 0

# Esta función recibe la fila y columna de una baldosa y nos devuelve
# un objeto que representa la baldosa en esa posición de la grilla.
def tile(col, row):
    # Primero chequeamos si la baldosa existe en la grilla, en cuyo 
    # caso la devolvemos
    if (col, row) in grid: return grid[(col, row)]

    # Si no existe, significa que estamos visitando una baldosa nueva,
    # creamos un objeto que guarda la información que sabemos hasta 
    # ahora de la baldosa (esencialmente, su ubicación).
    # Además dejamos la estructura preparada para poder "conectar" la
    # baldosa con sus vecinas (si las hubiera)
    t = {"col": col, 
         "row": row,
         "visited": False, # Distinguimos baldosas visitadas
         "up": None,
         "down": None,
         "left": None,
         "right": None}

    # Agregamos la baldosa a la grilla en la posición determinada
    grid[(col, row)] = t
    return t # Devolvemos la baldosa

# Esta función recibe dos baldosas y devuelve el valor de dirección que
# existe entre ellas. Las direcciones posibles son arriba (UP), abajo (DOWN),
# izquierda (LEFT), y derecha (RIGHT). Si no se encuentra una dirección 
# posible (porque es la misma baldosa o están en diagonal, por ejemplo), 
# esta función devuelve None 
def getDirectionBetween(src, dst):
    sc = src["col"]
    sr = src["row"]
    dc = dst["col"]
    dr = dst["row"]
    if dc - sc == 0: # Misma columna
        if dr - sr > 0: return Direction.DOWN
        if dr - sr < 0: return Direction.UP
    elif dr - sr == 0: # Misma fila
        if dc - sc > 0: return Direction.RIGHT
        if dc - sc < 0: return Direction.LEFT
    return None

# Esta función recibe dos baldosas, calcula la dirección en la que 
# debería avanzar el robot para moverse de una a la otra y luego 
# actualiza los atributos de cada una para reflejar el hecho de que 
# la navegación entre ellas es posible. La variable "src" representa 
# la baldosa de origen y "dst" la baldosa destino.
def connectTiles(src, dst):
    direction = getDirectionBetween(src, dst)
    if direction == Direction.UP:
        src["up"] = dst
        dst["down"] = src
    elif direction == Direction.RIGHT: 
        src["right"] = dst
        dst["left"] = src
    elif direction == Direction.DOWN:
        src["down"] = dst
        dst["up"] = src
    elif direction == Direction.LEFT:
        src["left"] = dst
        dst["right"] = src

# Esta función devuelve True si la baldosa está conectada con alguna baldosa 
# vecina (no importa en qué dirección).
def isConnected(tile):
    return tile["up"] != None or tile["down"] != None \
        or tile["left"] != None or tile["right"] != None

# Esta función escribe en un archivo de texto una representación del mapa
# trazado hasta ahora por el robot. 
# IMPORTANTE: Este formato NO es el que usa el supervisor de erebus para
# otorgar los puntos. Es necesario aplicar un algoritmo de transformación
# para generar la matriz correcta. Sin embargo, usaremos esta representación
# como una forma rápida de verificar manualmente el mapa trazado.
def writeGrid():
    # Primero buscamos los extremos del mapa, que nos servirá para iterar
    # en la grilla en el orden correcto.
    min_col, min_row, max_col, max_row = 0, 0, 0, 0
    for c, r in grid:
        t = grid.get((c, r))
        if t == None or not isConnected(t): continue # Ignoramos baldosas aisladas
        if c < min_col: min_col = c
        if r < min_row: min_row = r
        if c > max_col: max_col = c
        if r > max_row: max_row = r

    # Luego revisamos una por una cada baldosa y calculamos los caracteres
    # a imprimir de acuerdo a sus características (si es la baldosa de
    # inicio, si tiene vecinos cuáles, si fue visitada, etc.)
    char_groups = []
    for r in range(min_row, max_row + 1):
        char_group = []
        for c in range(min_col, max_col + 1):
            t = grid.get((c, r))
            chars = [["+", "-", "+"],
                     ["|", "X", "|"],
                     ["+", "-", "+"]]
            if t != None:
                if c == col and r == row:
                    if direction == Direction.UP:
                        chars[1][1] = "U"
                    elif direction == Direction.DOWN:
                        chars[1][1] = "D"
                    elif direction == Direction.LEFT:
                        chars[1][1] = "L"
                    elif direction == Direction.RIGHT:
                        chars[1][1] = "R"
                elif c == 0 and r == 0:
                    chars[1][1] = "@"
                elif not isConnected(t):
                    chars[1][1] = "X"
                elif not t["visited"]:
                    chars[1][1] = "?"
                else:
                    chars[1][1] = " "
                
                if t["up"] != None: chars[0][1] = " "
                if t["right"] != None: chars[1][2] = " "
                if t["down"] != None: chars[2][1] = " "
                if t["left"] != None: chars[1][0] = " "
            char_group.append(chars)
        char_groups.append(char_group)
    
    # Finalmente, abrimos el archivo y escribimos los caracteres que
    # representan a cada baldosa
    with open(FILE, "w") as f:
        for char_group in char_groups:
            for i in range(0, 3):
                for chars in char_group:
                    f.write("".join(chars[i]))
                f.write("\n")

# Esta función lee el valor del gps y actualiza la variable "position"
def updatePosition():
    global position, initialPosition
    x, _, y = gps.getValues()
    position = {"x": x, "y": y}

# Esta función transforma una dirección (UP/DOWN/LEFT/RIGHT) en su
# correspondiente ángulo (en radianes)
def directionToAngle(dir):
    if dir == Direction.UP: return math.tau/4
    if dir == Direction.RIGHT: return 0
    if dir == Direction.DOWN: return -math.tau/4
    if dir == Direction.LEFT: return math.tau/2

# Esta función lee el valor del giroscopio y actualiza la variables: 
# "rotation", "direction", y "currentTime" (esta última es necesaria
# para realizar correctamente el cálculo de rotación)
def updateRotation():
    global currentTime, rotation, direction
    lastTime = currentTime
    currentTime = robot.getTime()
    deltaTime = currentTime - lastTime
    
    vel, _, _ = gyro.getValues()
    rotation += (vel * deltaTime)
    rotation %= math.tau
    
    # Dependiendo del ángulo en el que quedó orientado el robot, 
    # actualizamos el valor de dirección
    for dir in Direction:
        if angle_diff(rotation, directionToAngle(dir)) < math.tau/8:
            direction = dir
            break # Ya encontramos la dirección, podemos salir

def updateVars():
    updatePosition()
    updateRotation()

def step():
    result = robot.step(TIME_STEP)
    updateVars()
    return result

def delay(ms):
    initTime = robot.getTime()
    while step() != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

def angle_diff(a, b):
    clockwise = (a - b) % math.tau
    counterclockwise = (b - a) % math.tau
    return min(clockwise, counterclockwise)

def girar(rad):
    lastRot = rotation
    deltaRot = 0

    while step() != -1:
        deltaRot += angle_diff(rotation, lastRot)
        lastRot = rotation

        diff = angle_diff(deltaRot, abs(rad))

        mul = (5/math.pi) * diff
        mul = min(max(mul, 0.1), 1)

        if rad > 0:
            wheelL.setVelocity(mul*MAX_VEL)
            wheelR.setVelocity(-mul*MAX_VEL)
        else:
            wheelL.setVelocity(-mul*MAX_VEL)
            wheelR.setVelocity(mul*MAX_VEL)

        if diff <= 0.01:
            break

    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

def dist(pt1, pt2):
    return math.sqrt((pt2["x"]-pt1["x"])**2 + (pt2["y"]-pt1["y"])**2)

def avanzar(distance):
    initPos = position

    while step() != -1:
        diff = abs(distance) - dist(position, initPos) 

        vel = min(max(diff/0.01, 0.1), 1)
        if distance < 0: vel *= -1
        
        wheelL.setVelocity(vel*MAX_VEL)
        wheelR.setVelocity(vel*MAX_VEL)

        if diff < 0.001:
            break
    
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

# Esta función devuelve las baldosas vecinas a la baldosa actual (cur_tile).
# Siempre las devuelve en el mismo orden relativo a la orientación del robot:
# izquierda, adelante, derecha, y por último atrás. Esto es importante porque
# luego usaremos esta lista de baldosas como candidatas para mover al robot.
# Para determinar si las baldosas están conectadas usamos los sensores de 
# distancia en busca de paredes. Sólo devolvemos aquellas baldosas que estén
# conectadas con la baldosa actual. 
def checkNeighbours(cur_tile):
    col = cur_tile["col"]
    row = cur_tile["row"]

    # Dependiendo de la orientación del robot vamos a buscar las baldosas relativas a la
    # posición actual en el siguiente orden.
    # U: (-1, 0), (0, -1), (1, 0), (0, 1)
    # R: (0, -1), (1, 0), (0, 1), (-1, 0)
    # D: (1, 0), (0, 1), (-1, 0), (0, -1)
    # L: (0, 1), (-1, 0), (0, -1), (1, 0)
    tiles = None
    if direction == direction.UP:
        tiles = list(tile(col + c, row + r) for c, r in ((-1, 0), (0, -1), (1, 0), (0, 1)))
    elif direction == direction.RIGHT:
        tiles = list(tile(col + c, row + r) for c, r in ((0, -1), (1, 0), (0, 1), (-1, 0)))
    elif direction == direction.DOWN:
        tiles = list(tile(col + c, row + r) for c, r in ((1, 0), (0, 1), (-1, 0), (0, -1)))
    elif direction == direction.LEFT:
        tiles = list(tile(col + c, row + r) for c, r in ((0, 1), (-1, 0), (0, -1), (1, 0)))
    
    # Ahora que tenemos la lista de baldosas vecinas eliminamos aquellas que no estén
    # conectadas con la actual. Para eso simplemente chequeamos los sensores de distancia
    # buscando paredes que imposibiliten el camino.
    sensors = (ps5, ps7, ps2, ps4)
    for i in range(4):
        if sensors[i].getValue() < 0.1:
            tiles[i] = None
    
    # Finalmente eliminamos los valores nulos y devolvemos la lista resultante
    return list(filter(None, tiles))

# Esta función mueve al robot desde la baldosa actual (cur_tile) hasta la baldosa a la que 
# queremos ir (next_tile). Ambas baldosas DEBEN ser vecinas y estar conectadas. De lo contrario,
# el comportamiento será inválido.
def move(cur_tile, next_tile):
    # Primero calculamos la dirección entre las baldosas (UP/DOWN/LEFT/RIGHT)
    dir = getDirectionBetween(cur_tile, next_tile)

    # Luego calculamos el ángulo correspondiente a esa dirección
    angle = directionToAngle(dir)

    # Giramos el robot en la dirección que implique el menor giro
    clockwise = (rotation - angle) % math.tau
    counterclockwise = (angle - rotation) % math.tau
    if clockwise < counterclockwise:
        girar(clockwise)
    else:
        girar(-counterclockwise)

    # Y finalmente avanzamos la distancia de 1 baldosa
    avanzar(0.12)

while step() != -1:
    # Primero marcamos la baldosa actual como visitada
    cur_tile = tile(col, row)
    cur_tile["visited"] = True

    # Luego nos fijamos a dónde podemos movernos. La función checkNeighbours() devuelve
    # las baldosas siempre en el mismo orden: izq, adelante, derecha, atrás. 
    # De esta forma, se privilegia girar hacia la izquierda
    candidates = checkNeighbours(cur_tile)

    # Si la lista de baldosas vecinas está vacía significa que no podemos ir a ningún lado
    if len(candidates) == 0:
        print("ERROR! No tengo adonde ir!")
        break

    # Conectamos la baldosa actual con las vecinas
    for candidate in candidates:
        connectTiles(cur_tile, candidate)

    # Elegimos una baldosa para movernos (preferiblemente no visitada)
    next_tile = next((tile for tile in candidates if not tile["visited"]), candidates[0])
    
    # Movemos el robot hacia la baldosa elegida
    move(cur_tile, next_tile)

    # Actualizamos col y row
    col = next_tile["col"]
    row = next_tile["row"]

    # (OPCIONAL) Escribimos el mapa en un archivo para poder validarlo rápidamente
    writeGrid()
    
    # (OPCIONAL) Mostramos en consola la dirección y ubicación del robot
    print(direction)
    print([col, row])
    print("-----------")