# Ejemplo: Calculando la rotación del robot usando la unidad de medición inercial
from controller import Robot
import math # Vamos a referirnos a algunas constantes matemáticas

TIME_STEP = 16
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

# Inicializamos la unidad de medición inercial
inertialUnit = robot.getDevice("inertial_unit")
inertialUnit.enable(TIME_STEP)

# Esta variable va a tener la orientación del robot (en radianes)
rotation = None

# La función updateVars() se encarga de actualizar las variables globales 
# de acuerdo a los valores de los sensores. 
# IMPORTANTE: Hay que llamarla después de cada robot.step()
def updateVars():
    global rotation
    
    # 1) Obtenemos la rotación del robot en los tres ejes
    roll, pitch, yaw = inertialUnit.getRollPitchYaw()    
    print(f"Roll: {roll:.3f}, Pitch: {pitch:.3f}, Yaw: {yaw:.3f}")

    # 2) El eje que nos interesa para la rotación del robot es el yaw
    rotation = yaw

    # 3) Normalizamos el valor de rotation para que se mantenga siempre entre
    # 0 y 360 grados (o el equivalente en radianes: 0 y 2*PI)
    rotation %= math.tau # Normalizamos el valor del ángulo

    # OPCIONAL: Calcular el valor de rotación en grados y mostrarlo en consola
    degrees = rotation * 180/math.pi
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