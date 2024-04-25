# Ejercicio 2: Avanzar un determinado tiempo y retroceder al inicio
from controller import Robot 

# Estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28

# Creamos la instancia del controlador del robot
robot = Robot()

# Creamos los objetos para controlar las ruedas
wheelL = robot.getDevice("wheel1 motor")
wheelR = robot.getDevice("wheel2 motor")

# Definimos la rotación de las ruedas para que sea infinita
wheelL.setPosition(float("inf"))
wheelR.setPosition(float("inf"))

# Esta función sirve para que el robot no haga caso a ninguna nueva 
# instrucción durante un tiempo determinado
def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

# Funciones nuevas
# Avanza en línea recta
def avanzar():
    wheelL.setVelocity(MAX_VEL)
    wheelR.setVelocity(MAX_VEL)

# Retrocede en línea recta
def retroceder():
    wheelL.setVelocity(MAX_VEL * -1)
    wheelR.setVelocity(MAX_VEL * -1)

# Loop principal
while robot.step(TIME_STEP) != -1: 
    avanzar()
    delay(1600)
    retroceder()    
    delay(1600)