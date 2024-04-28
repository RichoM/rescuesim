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

ps5 = robot.getDevice("ps5")
ps5.enable(TIME_STEP)

def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 >= ms:
            break

def turnRight():
    wheelL.setVelocity(MAX_VEL)
    wheelR.setVelocity(-MAX_VEL)
    delay(350)
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(1)

def turnLeft():
    wheelL.setVelocity(0.30*MAX_VEL)
    wheelR.setVelocity(1.00*MAX_VEL)
    delay(350)
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(1)

while robot.step(TIME_STEP) != -1:
    # Leo los sensores de distancia y guardo los valores en variables
    dist_left = ps5.getValue()
    dist_front = ps7.getValue()

    # Ajustamos la velocidad de las ruedas dependiendo de la distancia
    # con la pared izquierda. Si nos acercamos mucho giramos ligeramente
    # a la derecha. Si nos alejamos giramos ligeramente a la izquierda.
    # El objetivo es mantenernos en un rango entre 0.035 y 0.045
    if dist_left < 0.035:
        wheelL.setVelocity(1.0 * MAX_VEL)
        wheelR.setVelocity(.95 * MAX_VEL)
    elif dist_left > 0.045:
        wheelL.setVelocity(.95 * MAX_VEL)
        wheelR.setVelocity(1.0 * MAX_VEL)
    else:
        wheelL.setVelocity(1.0 * MAX_VEL)
        wheelR.setVelocity(1.0 * MAX_VEL)

    # Si la distancia a la pared izquierda supera los 0.1 metros
    # significa que tenemos que girar 90 grados hacia la izquierda.
    # Si en cambio nos encontramos con una pared adelante, tenemos
    # que girar 90 grados a la derecha.
    if dist_left > 0.1:
        turnLeft()
    elif dist_front < 0.05:
        turnRight()
        