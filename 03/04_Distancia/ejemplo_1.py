# Ejemplo: Mostrando el valor del sensor ps0
from controller import Robot

TIME_STEP = 32

robot = Robot()

ps0 = robot.getDevice("ps0") # Paso 1
ps0.enable(TIME_STEP) # Paso 2

while robot.step(TIME_STEP) != -1:
    dist = ps0.getValue() # Paso 3
    print(f"Distancia: {dist}")