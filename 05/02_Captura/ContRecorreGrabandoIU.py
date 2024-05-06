from controller import Robot
import math
import cv2
import numpy as np

TIME_STEP = 32
MAX_VEL = 6.28
robot = Robot()


position = None
initialPosition = None
rotation = 0
beginTime = robot.getTime()
currentTime = beginTime
deltaTime = 0

x = 0
y = 0

gps=robot.getDevice("gps")
gps.enable(TIME_STEP)

iu=robot.getDevice("inertial_unit")
iu.enable(TIME_STEP)

ruedaI = robot.getDevice("ruedaI motor")
ruedaI.setPosition(float("inf"))

ruedaD = robot.getDevice("ruedaD motor")
ruedaD.setPosition(float("inf"))

di = robot.getDevice("distanciaIzquierda")
di.enable(TIME_STEP)

dd = robot.getDevice("distanciaDerecha")
dd.enable(TIME_STEP)

df=robot.getDevice("distanciaFrente")
df.enable(TIME_STEP)

camI=robot.getDevice("camaraIzquierda")
camI.enable(TIME_STEP)

camD=robot.getDevice("camaraDerecha")
camD.enable(TIME_STEP)

camF=robot.getDevice("camaraFrente")
camF.enable(TIME_STEP)

def updatePosition():
    global position
    x, _, y = gps.getValues()
    position = {"x": x, "y": y}

def updateRotation():
    global rotation
    _, _, rotation = iu.getRollPitchYaw()
    # OPCIONAL: Calcular el valor de rotación en grados y mostrarlo en consola
    # degrees = rotation * 180/math.pi
    # print(f"Velocidad: {vel:.3f} rad/s")
    # print(f"Rotación: {rotation:.3f} rad ({degrees:.3f} deg)")
    # print("================")
    
def updateVars():
    updatePosition()
    updateRotation()
    
    

def step():
    result = robot.step(TIME_STEP)
    updateVars()
    return result

def delay(ms):
    initTime = robot.getTime()
    while step() != -1:
        if (robot.getTime() - initTime) * 1000.0 >= ms:
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

        if diff <= 0.01:
            break

        mul = (4/math.pi) * diff
        mul = min(max(mul, 0.1), 1)

        if rad > 0:
            ruedaI.setVelocity(mul*MAX_VEL)
            ruedaD.setVelocity(-mul*MAX_VEL)
        else:
            ruedaI.setVelocity(-mul*MAX_VEL)
            ruedaD.setVelocity(mul*MAX_VEL)



    ruedaI.setVelocity(0)
    ruedaD.setVelocity(0)

def dist(pt1, pt2):
    return math.sqrt((pt2["x"]-pt1["x"])**2 + (pt2["y"]-pt1["y"])**2)

def avanzar(distance):
    initPos = position

    while step() != -1:
        grabar()
        diff = abs(distance) - dist(position, initPos) 

        vel = min(max(diff/0.01, 0.1), 1)
        if distance < 0: vel *= -1
        
        ruedaI.setVelocity(vel*MAX_VEL)
        ruedaD.setVelocity(vel*MAX_VEL)

        if diff < 0.001:
            break
    
    ruedaI.setVelocity(0)
    ruedaD.setVelocity(0)

nroImagen=0
pasoGrabacion=0
CADACUANTOGRABO=5
def convertirCamara(imagen, alto, ancho): #Convierte la imagen de la camara a una imagen de opencv
    return np.array(np.frombuffer(imagen, np.uint8).reshape((alto,ancho, 4)))

def grabar():
    global nroImagen, pasoGrabacion
    pasoGrabacion+=1
    if pasoGrabacion==CADACUANTOGRABO:
        pasoGrabacion=0
        nroImagen+=1
        cv2.imwrite(f"CI{str(nroImagen).rjust(4,'0')}.png",convertirCamara(camI.getImage(), 40,40))
        cv2.imwrite(f"CD{str(nroImagen).rjust(4,'0')}.png",convertirCamara(camD.getImage(),40,40))
        cv2.imwrite(f"CF{str(nroImagen).rjust(4,'0')}.png",convertirCamara(camF.getImage(),128,128))

ruedaI.setVelocity(0)
ruedaD.setVelocity(0)
step() #Ejecuto una vez la simulación para tener valores iniciales de sensores
initialPosition = position

while step() != -1:
    distI=di.getValue()
    distD=dd.getValue()
    distF=df.getValue()


    if(distI>0.13):
        girar(-0.25*math.tau) #giro a la izquierda 90 grados
        avanzar(0.12) #medida de un mosaico
    elif(distF<0.13):
        girar(0.25*math.tau) #giro a la derecha 90 grados
    else:
        avanzar(0.12) #medida de un mosaico

    delay(200)
