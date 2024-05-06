# Ejemplo: Imprimir valores del GPS
from controller import Robot

TIME_STEP = 32

robot = Robot() 

gps = robot.getDevice("gps") # Paso 1: Obtener el sensor
gps.enable(TIME_STEP) # Paso 2: Habilitar el sensor

while robot.step(TIME_STEP) != -1:
    # Paso 3: Usar el método getValues() para obtener la posición del robot (x, y, z)
    x, y, z = gps.getValues()
    
    print(f"X: {x:.3f}, Y: {y:.3f}, Z: {z:.3f}")