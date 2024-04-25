# Ejemplo: usando el encoder del motor izquierdo
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28 # Velocidad máxima (1 vuelta por segundo)

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

encoderL = wheelL.getPositionSensor() # Paso 1
encoderL.enable(TIME_STEP) # Paso 2

while robot.step(TIME_STEP) != -1:
    wheelL.setVelocity(0.1*MAX_VEL)

    pos = encoderL.getValue() # Paso 3
    print(f"La posición del motor es {pos} radianes")