# Ejemplo: Imprimir el color RGB que ve el sensor de color
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

# Obtener el sensor de color y habilitarlo
colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(TIME_STEP)

while robot.step(TIME_STEP) != -1:
    # Acceder al color detectado por el sensor. El canal A lo ignoramos.
    b, g, r, a = colorSensor.getImage()

    print(f"R: {r}, G: {g}, B: {b}")
