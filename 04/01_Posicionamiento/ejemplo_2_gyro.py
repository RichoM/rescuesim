# Ejemplo: Calculando la rotación del robot usando el giroscopio
from controller import Robot
import math # Vamos a referirnos a algunas constantes matemáticas

TIME_STEP = 16
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

# Inicializamos el giroscopio
gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)

# Esta variable va a tener la orientación del robot (en radianes).
rotation = 0

# Necesitamos algunas variables más para llevar la cuenta del tiempo de la 
# simulación, y cuánto tiempo pasó desde el último ciclo
beginTime = robot.getTime()
currentTime = beginTime
deltaTime = 0

# La función updateVars() se encarga de actualizar las variables globales 
# de acuerdo a los valores de los sensores. 
# IMPORTANTE: Hay que llamarla después de cada robot.step()
def updateVars():
    global currentTime, deltaTime, rotation
    # Primero calculamos cuánto tiempo pasó desde el último ciclo
    lastTime = currentTime
    currentTime = robot.getTime()
    deltaTime = currentTime - lastTime
    
    # Luego calculamos la rotación del robot:
    # 1) Obtenemos primero la velocidad angular
    _, vel, _ = gyro.getValues()
    
    # 2) Calculamos luego la rotación en el último ciclo y la sumamos a la 
    # variable rotation
    rotation += (vel * deltaTime)
    # 3) Normalizamos el valor de rotation para que se mantenga siempre entre
    # 0 y 360 grados (o el equivalente en radianes: 0 y 2*PI)
    rotation %= math.tau # Normalizamos el valor del ángulo
    
    # OPCIONAL: Calcular el valor de rotación en grados y mostrarlo en consola
    degrees = rotation * 180/math.pi
    print(f"Velocidad: {vel:.3f} rad/s")
    print(f"Rotación: {rotation:.3f} rad ({degrees:.3f} deg)")
    print("================")

# Encapsulamos la llamada a robot.step() en una función step() propia que llama 
# automáticamente a updateVars(). De esta forma evitamos llamar a updateVars() 
# manualmente porque step() lo hace por nosotros.
def step():
    result = robot.step(TIME_STEP)
    updateVars()
    return result

# Tenemos que actualizar delay() para que llame a nuestra función step() en
# lugar de robot.step()
def delay(ms):
    initTime = robot.getTime()
    while step() != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

# En lugar de llamar a robot.step() llamamos a nuestra función step()
while step() != -1:
    wheelL.setVelocity(-0.25*MAX_VEL)
    wheelR.setVelocity(0.25*MAX_VEL)
    delay(500)
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(500)

    

