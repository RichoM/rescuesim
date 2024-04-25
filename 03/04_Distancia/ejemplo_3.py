# Ejemplo: Manteniendo torpemente la distancia con la pared
# Usar mundo cuadrado_1.wbt
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor")
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor")
wheelR.setPosition(float("inf"))

ps6 = robot.getDevice("ps6")
ps6.enable(TIME_STEP)

ps5 = robot.getDevice("ps5")
ps5.enable(TIME_STEP)

delta0 = None # Declaramos la variable delta0

while robot.step(TIME_STEP) != -1:
    if delta0 == None: # Sólo en el primer ciclo, inicializamos delta0
        delta0 = ps6.getValue() - ps5.getValue()
    
    # Calculamos la diferencia con la medición inicial
    giro = (ps6.getValue() - ps5.getValue()) - delta0
    
    # Avanzamos dependiendo del signo de "giro"
    # giro positivo = izquierda
    # giro negativo = derecha
    if giro > 0:
        wheelL.setVelocity(0.5*MAX_VEL)
        wheelR.setVelocity(1.0*MAX_VEL)
    else:
        wheelL.setVelocity(1.0*MAX_VEL)
        wheelR.setVelocity(0.5*MAX_VEL)

    # Si nos acercamos mucho a la pared, giramos rápidamente
    if ps6.getValue() < 0.06:
        wheelL.setVelocity(1.0*MAX_VEL)
        wheelR.setVelocity(-1.0*MAX_VEL)