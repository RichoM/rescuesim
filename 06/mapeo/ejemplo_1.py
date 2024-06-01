# Ejemplo 1: Trazando un mapa básico
from controller import Robot
from enum import Enum
import math
from random import random

TIME_STEP = 32
MAX_VEL = 6.28

# En este archivo vamos a escribir la representación textual del mapa 
# trazado a medida que recorremos el laberinto.
# IMPORTANTE: Cambiar el valor de esta cadena de texto para que apunte
# a una carpeta válida en el sistema (de otra forma, dará error)
FILE = r"X:\RoboCupRescue\temp\map.txt"

# Declaramos las 4 direcciones en las que puede estar "mirando" el robot
class Direction(Enum):
    UP = 1      # Arriba
    DOWN = 2    # Abajo
    LEFT = 3    # Izquierda
    RIGHT = 4   # Derecha

robot = Robot() 

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

# Usaremos el sensor de distancia ps7 para no chocar con la pared
ps7 = robot.getDevice("ps7")
ps7.enable(TIME_STEP)

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
         "up": None,
         "down": None,
         "left": None,
         "right": None}

    # Agregamos la baldosa a la grilla en la posición determinada
    grid[(col, row)] = t
    return t # Devolvemos la baldosa

# Esta función recibe dos baldosas y la dirección de movimiento del
# robot y actualiza sus atributos para reflejar el hecho de que es
# posible moverse de una a otra. La variable "src" representa la 
# baldosa de origen y "dst" la baldosa destino.
def connectTiles(src, dst, direction):
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
        if c < min_col: min_col = c
        if r < min_row: min_row = r
        if c > max_col: max_col = c
        if r > max_row: max_row = r

    # Luego revisamos una por una cada baldosa y calculamos los caracteres
    # a imprimir de acuerdo a sus características (si es la baldosa de
    # inicio, si tiene vecinos cuáles, etc.)
    rows = []
    for r in range(min_row, max_row + 1):
        row = []
        for c in range(min_col, max_col + 1):
            t = grid.get((c, r))
            chars = [["+", "-", "+"],["|", "?", "|"],["+", "-", "+"]]
            if t != None:
                chars[1][1] = "@" if c == 0 and r == 0 else " "
                if t["up"] != None: chars[0][1] = " "
                if t["right"] != None: chars[1][2] = " "
                if t["down"] != None: chars[2][1] = " "
                if t["left"] != None: chars[1][0] = " "
            row.append(chars)
        rows.append(row)
    
    # Finalmente, abrimos el archivo y escribimos los caracteres que
    # representan a cada baldosa
    with open(FILE, "w") as f:
        for row in rows:
            for i in range(0, 3):
                for chars in row:
                    f.write("".join(chars[i]))
                f.write("\n")

# Esta función lee el valor del gps y actualiza la variable "position"
def updatePosition():
    global position, initialPosition
    x, _, y = gps.getValues()
    position = {"x": x, "y": y}

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
    if angle_diff(rotation, math.tau/4) < math.tau/8: 
        direction = Direction.UP
    elif angle_diff(rotation, 0) < math.tau/8: 
        direction = Direction.RIGHT
    elif angle_diff(rotation, -math.tau/4) < math.tau/8: 
        direction = Direction.DOWN
    elif angle_diff(rotation, math.tau/2) < math.tau/8: 
        direction = Direction.LEFT
    
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

while step() != -1:
    # Primero chequeamos el valor del sensor delantero
    if ps7.getValue() < 0.08:
        # Si encontramos una pared giramos 90 grados hacia
        # la izquierda o la derecha al azar        
        if random() < 0.5:
            girar(0.25*math.tau) # Girar derecha
        else:
            girar(-0.25*math.tau) # Girar izquierda
    else:
        # Si el camino está despejado entonces avanzamos, pero primero
        # registramos en una variable la baldosa en la que estamos ahora
        # (antes de realizar el movimiento)
        prev = tile(col, row)

        # Avanzamos 0.12 m (es decir, una baldosa)
        avanzar(0.12)
            
        # Actualizamos el valor de col o row dependiendo del movimiento que
        # haya hecho el robot
        if direction == Direction.UP: row -= 1
        elif direction == Direction.RIGHT: col += 1
        elif direction == Direction.DOWN: row += 1
        elif direction == Direction.LEFT: col -= 1
        
        # Luego vamos a buscar a la grilla la baldosa actual (luego de
        # haber avanzado)
        cur = tile(col, row)

        # Conectamos ambas baldosas teniendo en cuenta la dirección en la
        # que avanzó el robot
        connectTiles(prev, cur, direction)

        # Y finalmente escribimos el mapa en un archivo
        writeGrid()

    # (OPCIONAL) Mostramos en consola la dirección y ubicación del robot
    print(direction)
    print([col, row])
    print("-----------")