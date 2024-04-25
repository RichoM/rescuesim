# Control de los motores

Para controlar los motores debemos seguir los siguientes pasos:

1. Obtener un objeto Motor para cada motor que vayamos a utilizar. Es conveniente guardar este objeto en una variable de forma que podamos usarlo más adelante para referirnos al mismo.
2. Establecer la posición de cada motor en infinito para que los mismos puedan girar libremente, sin detenerse en una posición determinada.
3. Establecer la velocidad a la que queremos que el motor gire (en [radianes](https://es.wikipedia.org/wiki/Radi%C3%A1n) por segundo)


> NOTA: Los radianes son una forma de medir ángulos al igual que los grados sexagesimales. Podemos convertir entre radianes y grados usando las siguientes fórmulas:
>
> * radianes = grados * PI / 180
> * grados = radianes * 180 / PI


Para obtener cada objeto Motor debemos ejecutar el método `robot.getDevice` pasando como parámetro el nombre del motor:

* Para el motor izquierdo: “wheel1 motor”
* Para el motor derecho: “wheel2 motor”

## Ejemplo 1 - Prendiendo motores

En el siguiente ejemplo se pueden observar los 3 pasos antes mencionados para mover el motor izquierdo a la máxima velocidad permitida.

```python
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28 # Velocidad máxima (1 vuelta por segundo)

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") # Paso 1 
wheelL.setPosition(float("inf")) # Paso 2

while robot.step(TIME_STEP) != -1:
    wheelL.setVelocity(MAX_VEL) # Paso 3
```

La velocidad máxima de cada motor es 6,28 radianes/s, lo cual equivale a una vuelta completa cada segundo. Si superamos la velocidad máxima webots muestra un error en la consola, por lo cual recomendamos usar una variable global (MAX_VEL, en este caso) para guardar la velocidad máxima y poder referirnos a ella a la hora de establecer la velocidad final del motor.

[Descargar ejemplo 1 completo](ejemplo_1.py)

## Ejemplo 2 - Avanzar

Para mover el robot en el mapa, sin embargo, no alcanza con controlar el motor izquierdo, necesitamos ambos motores. Dependiendo de la velocidad que asignemos a cada motor vamos a obtener diferentes tipos de movimientos.

Para avanzar, por ejemplo, debemos asignar la misma velocidad a ambos motores:

```python
wheelL.setVelocity(MAX_VEL)
wheelR.setVelocity(MAX_VEL)
```

[Descargar ejemplo 2 completo](ejemplo_2.py)

## Ejemplo 3 - Retroceder

Para retroceder usamos la misma velocidad en ambos motores, pero en sentido inverso (nótese el signo):

```python
wheelL.setVelocity(-MAX_VEL)
wheelR.setVelocity(-MAX_VEL)
```

[Descargar ejemplo 3 completo](ejemplo_3.py)

## Ejemplo 4 - Girar a la derecha

Si queremos hacer que el robot gire, vamos a asignar diferentes velocidades a cada motor. El tipo de giro más sencillo que podemos realizar es una rotación sobre el centro del robot. Para ello, asignamos la misma velocidad a cada motor pero en uno de los dos invertimos el signo (es decir, hacemos que uno de los dos motores gire en sentido contrario al otro). Dependiendo del sentido de giro que deseamos obtener, invertiremos uno u otro motor.

Para rotar en sentido horario (o hacia la derecha, visto desde la perspectiva del robot) debemos entonces invertir el sentido del motor derecho:

```python
wheelL.setVelocity(MAX_VEL)
wheelR.setVelocity(-MAX_VEL)
```

[Descargar ejemplo 4 completo](ejemplo_4.py)

## Ejemplo 5 - Girar a la izquierda

Por el contrario, si deseamos girar en sentido anti-horario (o hacia la izquierda), invertiremos el motor izquierdo:

```python
wheelL.setVelocity(-MAX_VEL)
wheelR.setVelocity(MAX_VEL)
```

[Descargar ejemplo 5 completo](ejemplo_5.py)

## Ejemplo 6 - Uso de los encoders

Los motores del robot e-puck incluyen también encoders que permiten determinar cuánto giró el motor. Para acceder a los valores de los encoders debemos seguir los siguientes pasos:

1. Obtener el objeto encoder del motor. Para ello usamos el método “motor.getPositionSensor”.
2. Habilitar el encoder usando el método “enable”. Este método espera un parámetro que debe ser la frecuencia de actualización del encoder (usualmente TIME_STEP).
3. Obtener el valor de rotación del encoder (en radianes). Importante: girar el motor hacia atrás decrementa este valor.

En el siguiente ejemplo habilitamos el encoder del motor izquierdo y mostramos en la consola su posición mientras el motor gira a un 10% de su velocidad máxima.

```python
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28 # Velocidad máxima (1 vuelta por segundo)

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

encoderL = wheelL.getPositionSensor() # Paso 1
encoderL.enable(TIME_STEP) # Paso 2

while robot.step(TIME_STEP) != -1:
    wheelL.setVelocity(0.1*MAX_VEL)

    pos = encoderL.getValue() # Paso 3
    print(f"La posición del motor es {pos} radianes")
```

[Descargar ejemplo 6 completo](ejemplo_6.py)

## Ejercicios

Para cada ejercicio se pide armar un programa controlador distinto y entregar los archivos de código.

1. Prender ambos motores a la mitad de la velocidad máxima.
2. Avanzar una distancia determinada y luego volver a la posición inicial.
3. Girar 90 grados en sentido horario y luego frenar.
4. Girar 180 grados en sentido antihorario y luego frenar.
5. Trazar un círculo con el movimiento del robot. IMPORTANTE: Usar el mundo "mapa_circulito.wbt"
