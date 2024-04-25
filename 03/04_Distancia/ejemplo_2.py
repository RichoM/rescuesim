# Ejemplo: Avanzar hasta encontrar una pared
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor")
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor")
wheelR.setPosition(float("inf"))

ps7 = robot.getDevice("ps7")
ps7.enable(TIME_STEP)

ps0 = robot.getDevice("ps0")
ps0.enable(TIME_STEP)

while robot.step(TIME_STEP) != -1:
    # Si detectamos una pared, nos detenemos
    if ps7.getValue() < 0.06 or ps0.getValue() < 0.06:
        wheelL.setVelocity(0)
        wheelR.setVelocity(0)
    else:
        wheelL.setVelocity(MAX_VEL)
        wheelR.setVelocity(MAX_VEL)