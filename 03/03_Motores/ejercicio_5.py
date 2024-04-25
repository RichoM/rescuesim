# Ejercicio 5: Trazar un círculo con el robot
# IMPORTANTE: Usar mapa_circulito.wbt
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

# Loop principal
while robot.step(TIME_STEP) != -1:
    wheelL.setVelocity(1.0 * MAX_VEL)
    wheelR.setVelocity(0.6 * MAX_VEL)