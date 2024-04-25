# Ejemplo de uso de la consola para mostrar el valor 
# de una variable
from controller import Robot

TIME_STEP = 32
robot = Robot()

while robot.step(TIME_STEP) != -1:
    print(robot.getTime()) # Muestro los segundos actuales en la consola