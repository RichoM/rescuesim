# Este controlador no hace nada pero muestra la estructura 
# básica del programa, la cual se va a repetir prácticamente
# en todos los ejemplos
from controller import Robot

TIME_STEP = 32
robot = Robot()

while robot.step(TIME_STEP) != -1:
    pass # Reemplazar por la lógica del controlador