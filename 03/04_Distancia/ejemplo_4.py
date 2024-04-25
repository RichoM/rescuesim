# Ejemplo: Habilitando todos los sensores de distancia  
from controller import Robot

TIME_STEP = 32

robot = Robot()

distSensors = []
for i in range(8):
    sensor = robot.getDevice("ps" + str(i))
    sensor.enable(TIME_STEP)
    distSensors.append(sensor)

while robot.step(TIME_STEP) != -1:
    for i in range(8):
        print(f"Distancia sensor {i}: {distSensors[i].getValue()}")
    print("================")