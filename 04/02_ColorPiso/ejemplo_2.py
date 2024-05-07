# Ejemplo: Detección de pantano usando el sensor de color
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

# Obtener el sensor de color y habilitarlo
colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(TIME_STEP)

def esPantano(r, g, b):
    # El color del pantano es (R:244, G:221, B:141), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 244) < 15 \
        and abs(g - 221) < 15 \
        and abs(b - 141) < 15

while robot.step(TIME_STEP) != -1:
    # Acceder al color detectado por el sensor. El canal A lo ignoramos.
    b, g, r, a = colorSensor.getImage()

    # Si llegamos a un pantano, mostramos un mensaje
    if esPantano(r, g, b):
        print(f"{robot.getTime():.2f}: Ojo! Pantano!")
