# Ejemplo: Moviendo el robot hacia atrás
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28 # Velocidad máxima (1 vuelta por segundo)

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

while robot.step(TIME_STEP) != -1:
    wheelL.setVelocity(-MAX_VEL)
    wheelR.setVelocity(-MAX_VEL)