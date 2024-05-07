# Ejemplo: Visualización de la info del LIDAR
# NOTA: Usar robot "robot_lidar.json"
from controller import Robot

# Vamos a usar NumPy para transformar la data del sensor en una imagen 
# y OpenCV para mostrarla en la pantalla
import numpy as np
import cv2

TIME_STEP = 32

robot = Robot()

lidar = robot.getDevice("lidar")
lidar.enable(TIME_STEP)

# Función para particionar una secuencia en listas de un tamaño máximo
def partition(seq, length):
    chunks = []
    chunk = []
    for e in seq:
        chunk.append(e)
        if len(chunk) == length:
            chunks.append(chunk)
            chunk = []
    if len(chunk) > 0:
        chunks.append(chunk)
    return chunks

# Función para "aplanar" una lista de listas
def flatten(t):
    return [item for sublist in t for item in sublist]

while robot.step(TIME_STEP) != -1:
    # Obtenemos la imagen
    image = lidar.getRangeImage()

    # Convertimos la información de profundidad en pixeles en escala de grises
    # y al mismo tiempo estiramos la imagen para que tenga 64 pixeles de alto
    pixels = []
    for d in flatten([p*32 for p in partition(image, 512)]):
        color = d * 255
        color = int(max(min(color, 255), 0))
        pixels.append(color)

    # Convertimos el array de pixeles en una imagen
    img = np.frombuffer(bytes(pixels), np.uint8).reshape((4*32, 512))

    # Mostramos la imagen en la pantalla
    cv2.imshow("lidar", img)
    cv2.waitKey(1)
    