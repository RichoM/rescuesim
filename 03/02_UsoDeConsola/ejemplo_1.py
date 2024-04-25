# Ejemplo de uso de la consola para mostrar un mensaje
# fijo en cada ciclo de la simulación
from controller import Robot

TIME_STEP = 32
robot = Robot()

while robot.step(TIME_STEP) != -1:
    print("Hola mundo")