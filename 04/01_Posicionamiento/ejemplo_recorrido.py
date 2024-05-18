# Ejercicio: Mejorar la estrategia de navegación usando las funciones
# de posicionamiento para avanzar y girar.
from controller import Robot
import math
from random import random

TIME_STEP = 16
MAX_VEL = 3.14 # Reduzco la velocidad para minimizar desvío

robot = Robot() 

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

lidar = robot.getDevice("lidar")
lidar.enable(TIME_STEP)

inertialUnit = robot.getDevice("inertial_unit")
inertialUnit.enable(TIME_STEP)

gps = robot.getDevice("gps")
gps.enable(TIME_STEP)

position = None
rotation = 0
rangeImage = None

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, point):
        dx = self.x-point.x
        dy = self.y-point.y
        return math.sqrt(dx**2 + dy**2)
    
    def __str__(self) -> str:
        return f"({self.x:.3f}, {self.y:.3f})"

def updatePosition():
    global position
    x, _, y = gps.getValues()
    position = Point(x, y)

def updateRotation():
    global rotation
    _, _, yaw = inertialUnit.getRollPitchYaw()
    rotation = yaw % math.tau # Normalizamos el valor del ángulo (0 a 2*PI)

def updateRangeImage():
    global rangeImage
    rangeImage = lidar.getRangeImage()[1024:1536]

def updateVars():
    updatePosition()
    updateRotation()
    updateRangeImage()
    print(f"Position: {position}, Rotation: {rotation:.3f} rad ({rotation*180/math.pi:.3f} deg)")

def step():
    result = robot.step(TIME_STEP)
    updateVars()
    return result

def delay(ms):
    initTime = robot.getTime()
    while step() != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

def angle_diff(a, b):
    clockwise = (a - b) % math.tau
    counterclockwise = (b - a) % math.tau
    return min(clockwise, counterclockwise)

def girar(rad):
    lastRot = rotation
    deltaRot = 0

    while step() != -1:
        deltaRot += angle_diff(rotation, lastRot)
        lastRot = rotation

        diff = angle_diff(deltaRot, abs(rad))

        mul = (5/math.pi) * diff
        mul = min(max(mul, 0.05), 1)

        if rad > 0:
            wheelL.setVelocity(mul*MAX_VEL)
            wheelR.setVelocity(-mul*MAX_VEL)
        else:
            wheelL.setVelocity(-mul*MAX_VEL)
            wheelR.setVelocity(mul*MAX_VEL)

        if diff <= 0.005:
            break

    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

def avanzar(distance):
    initPos = position

    while step() != -1:
        diff = abs(distance) - initPos.distance_to(position)

        vel = min(max(diff/0.01, 0.1), 1)
        if distance < 0: vel *= -1
        
        wheelL.setVelocity(vel*MAX_VEL)
        wheelR.setVelocity(vel*MAX_VEL)

        if diff < 0.001:
            break
    
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

def hayAlgoIzq():
    leftDist = rangeImage[128]
    return leftDist < 0.08

def hayAlgoDer():
    rightDist = rangeImage[128*3]
    return rightDist < 0.08

def hayAlgoAdelante():
    frontDist = rangeImage[256]
    return frontDist < 0.08

def girar_izq_90():
    girar(math.tau/4)

def girar_der_90():
    girar(-math.tau/4)

def girar_media_vuelta():
    girar(math.tau/2)

def avanzar_baldosa():
    avanzar(0.12)

wheelL.setVelocity(0)
wheelR.setVelocity(0)
step()

while step() != -1:
    if not hayAlgoIzq():
        girar_izq_90()
        avanzar_baldosa()
    elif not hayAlgoAdelante():
        avanzar_baldosa()
    elif not hayAlgoDer():
        girar_der_90()
        avanzar_baldosa()
    else:
        girar_media_vuelta()
        avanzar_baldosa()