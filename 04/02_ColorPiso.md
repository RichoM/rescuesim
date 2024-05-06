# 2. Detección del color del piso

El sensor de color de piso que posee el robot e-puck es, en realidad, una cámara RGB que captura una imagen de un pixel de ancho por un pixel de alto.

Usando la información de la cámara podemos identificar los diferentes tipos de baldosas que forman parte del mapa. En particular, nos interesa detectar:

* Pantanos
* Agujeros
* Conexiones entre áreas

Como cada tipo de baldosa tiene un color particular, podemos comparar la información obtenida por el sensor con los colores de las baldosas especiales y así determinar el tipo de baldosa sobre el que se encuentra el sensor.

Para usar el sensor de color tenemos que seguir los 3 pasos habituales:

1. Obtener el objeto que representa al sensor mediante el mensaje “robot.getDevice”. El nombre del sensor en el robot por defecto es “colour_sensor”.
2. Habilitar el sensor usando el mensaje “enable” pasando como parámetro el TIME_STEP de la simulación.
3. Acceder a los valores observador por el sensor mediando el mensaje “getImage”.

## Ejemplo 1 - Descomponer la imagen en canales RGB

Dado que el sensor de color es realmente una cámara, tenemos que utilizar el método “getImage” para acceder a la imagen que está observando el sensor. Esta imagen contiene únicamente 1 pixel así que podemos descomponerlo fácilmente en los canales RGB correspondientes.

La función “getImage()” devuelve un array con la información de cada píxel de la imagen. Cada pixel está compuesto por 4 bytes correspondientes a los canales azul (B), verde (G), rojo (R), y alpha (A). Dado que la imagen contiene sólo 1 pixel, nos interesan los primeros 3 valores del array (el canal A, que indica el grado de transparencia del píxel, lo ignoramos). 

```python
# Obtener el sensor de color y habilitarlo
colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(TIME_STEP)

while robot.step(TIME_STEP) != -1:
    # Acceder al color detectado por el sensor. El canal A lo ignoramos.
    b, g, r, a = colorSensor.getImage()

    print(f"R: {r}, G: {g}, B: {b}")
```

[Descargar ejemplo 1 completo](02_ColorPiso/ejemplo_1.py)

## Ejemplo 2 - Detección de pantanos

Una vez que podemos obtener el color detectado por el sensor en sus tres canales RGB resulta trivial usar este valor para identificar el tipo de baldosa que detecta el sensor.

Una forma sencilla consiste en apoyar el sensor sobre la baldosa a identificar para tomar nota del color de la misma. Es importante no guiarse únicamente por la imagen que muestra el simulador sino leer el valor observado por el sensor. Haciendo esto podemos verificar que el color del pantano es cercano a (R:244, G:221, B:141).

Luego, es sólo cuestión de comparar el valor detectado por el sensor con el que tenemos identificado como pantano. Es conveniente usar un umbral en la comparación para asegurarnos que la detección funcione incluso ante diferencias en la iluminación que modifiquen ligeramente el color del piso. 

```python
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
```

[Descargar ejemplo 2 completo](02_ColorPiso/ejemplo_2.py)

---

## Ejercicios

Para cada ejercicio se pide armar un programa controlador distinto y entregar los archivos de código.

1. Identificar los distintos tipos de baldosa e imprimir en consola el nombre (NO los valores de RGB!)
2. Hacer un robot que recorra el mapa [easy1.wbt](02_ColorPiso/easy1.wbt) y NO se caiga en agujeros.