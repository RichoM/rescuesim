# Ejemplo: movimiento del motor izquierdo
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28 # Velocidad máxima (1 vuelta por segundo)

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") # Paso 1 
wheelL.setPosition(float("inf")) # Paso 2

while robot.step(TIME_STEP) != -1:
    wheelL.setVelocity(MAX_VEL) # Paso 3