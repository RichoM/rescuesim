# Ejemplo de uso de la consola para mostrar el flujo
# de ejecución del programa
from controller import Robot

TIME_STEP = 32
robot = Robot()

print("Inició la simulación")

while robot.step(TIME_STEP) != -1:
    if True:
        print("Se está ejecutando la simulación")
    else:
        print("Este mensaje NO debería aparecer")

print("Terminó la simulación")