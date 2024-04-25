# Ejemplo de uso de la consola para mostrar el valor 
# de una variable usando "formatted strings"
from controller import Robot

TIME_STEP = 32
robot = Robot()

c = 0 # Usamos esta variable para contar los ciclos de simulación

while robot.step(TIME_STEP) != -1:
    c = c + 1 # En cada ciclo, incrementamos el contador en 1
    print(f"Cantidad de ciclos: {c}")
    print(f"Segundos de simulación: {robot.getTime()}")