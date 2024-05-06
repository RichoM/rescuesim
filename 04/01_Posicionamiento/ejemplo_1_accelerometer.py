# Ejemplo: Imprimir la aceleración del robot en la consola
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

# Creamos el objeto accelerometer y lo habilitamos
accel = robot.getDevice("accelerometer")
accel.enable(TIME_STEP)

# En esta variable vamos a guardar los valores que obtenemos del sensor
acceleration = [0, 0, 0]

def updateVars():
    global acceleration
    acceleration = accel.getValues()
    x, y, z = acceleration
    print(f"X: {x:.3f} m/s^2")    
    print(f"Y: {y:.3f} m/s^2")
    print(f"Z: {z:.3f} m/s^2")
    print("================")

def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        updateVars() # Llamamos a updateVars() luego de robot.step()
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

while robot.step(TIME_STEP) != -1:
    updateVars() # Llamamos a updateVars() luego de robot.step()

    wheelL.setVelocity(0.25*MAX_VEL)
    wheelR.setVelocity(0.25*MAX_VEL)
    delay(500)

    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(500)

    wheelL.setVelocity(1.0*MAX_VEL)
    wheelR.setVelocity(1.0*MAX_VEL)
    delay(500)

    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(500)
    

