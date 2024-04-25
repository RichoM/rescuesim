# Ejemplo del uso de la consola para mostrar un mensaje dependiendo
# de una condición
from controller import Robot

TIME_STEP = 32
robot = Robot()

t0 = robot.getTime() # Guardamos los segundos al iniciar el programa

while robot.step(TIME_STEP) != -1:
    # Chequeamos si pasaron 10 segundos.
    if robot.getTime() - t0 > 10:
        print("A") # Ya pasaron 10 segundos
        t0 = robot.getTime() # Vuelvo a iniciar el contador