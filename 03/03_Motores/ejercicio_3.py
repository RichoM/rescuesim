# Ejercicio 3: Girar 90 grados y luego frenar
from controller import Robot

# Estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28

# Creamos la instancia del controlador del robot
robot = Robot()

# Creamos los objetos para controlar las ruedas
wheelL = robot.getDevice("wheel1 motor")
wheelR = robot.getDevice("wheel2 motor")

# Definimos la rotación de las ruedas para que esa infinita
wheelL.setPosition(float("inf"))
wheelR.setPosition(float("inf"))

# Esta función sirve para que el robot no haga caso a ninguna nueva 
# instrucción durante un tiempo determinado
def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

# EL GIRO DEPENDE DE LA VELOCIDAD Y EL TIEMPO
# función girar 90 grados
def girar90():
    wheelL.setVelocity(0.5 * MAX_VEL)
    wheelR.setVelocity(-0.5 * MAX_VEL)
    delay(700)

def frenar():
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)   

# Loop principal
while robot.step(TIME_STEP) != -1:
    girar90()
    frenar()
    break # salgo del loop (termina el programa)
