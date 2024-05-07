# Ejemplo: Detección de obstáculos básica usando el LIDAR
# NOTA: Usar robot "robot_lidar.json"
from controller import Robot
import math

TIME_STEP = 32

robot = Robot()

lidar = robot.getDevice("lidar")
lidar.enable(TIME_STEP)

# Función que busca obstáculos en una capa del LIDAR
def hasObstacle(layer):
    # El LIDAR emite 512 rayos alrededor del robot, pero sólo nos interesan 
    # 5 puntos al frente del robot. Acá calculamos los índices de cada rayo 
    d = math.pi/16
    i0 = int((math.pi - d*4) / math.tau * 512)
    i1 = int((math.pi - d*1) / math.tau * 512)
    i2 = int((math.pi + d*0) / math.tau * 512)
    i3 = int((math.pi + d*1) / math.tau * 512)
    i4 = int((math.pi + d*4) / math.tau * 512)

    print(f"0: {layer[i0]:.3f}, 1: {layer[i1]:.3f}, 2: {layer[i2]:.3f}, 3: {layer[i3]:.3f}, 4: {layer[i4]:.3f}")

    # Umbrales para objetos cercanos y lejanos
    t_near = 0.06
    t_far = 0.2

    # Finalmente chequeamos que los rayos centrales (i1, i2, e i3) detecten
    # objeto cercano pero los extremos (i0 e i4) no detecten nada
    return (layer[i1] < t_near or layer[i2] < t_near or layer[i3] < t_near) \
        and (layer[i0] > t_far and layer[i4] > t_far)

while robot.step(TIME_STEP) != -1:
    # Obtenemos la imagen de profundidad
    image = lidar.getRangeImage()

    # Extraemos de la imagen sólo los datos correspondientes a la capa 1
    layer_1 = image[512:1024]

    # Si detectamos un obstáculo mostramos un mensaje
    if hasObstacle(layer_1):
        print("OBSTÁCULO!")
    else:
        print("NO HAY OBSTÁCULO")