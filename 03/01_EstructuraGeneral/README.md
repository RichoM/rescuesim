# Estructura general del programa

Para poder programar el comportamiento del robot es necesario escribir un archivo con código Python. Este archivo, llamado comúnmente “controlador”, tiene una serie de requisitos que debemos cumplir para que funcione correctamente.

En primer lugar, es necesario “importar” algunas clases importantes del espacio de nombres “controller”. Este espacio de nombres incluye clases útiles para poder controlar los motores y acceder a los valores de los sensores. Pero lo más importante de todo es que en este espacio de nombres se incluye la clase “Robot”, que necesitamos para interactuar con la simulación.

```python
from controller import Robot
```

Sin embargo, con sólo importar la clase Robot no alcanza. Tenemos que crear,  también, una instancia de Robot para poder llamar a los métodos correspondientes.

Lo más conveniente es entonces crear una instancia de Robot y guardarla en una variable, cómo se ve a continuación:

```python
robot = Robot()
```

De esta forma, cada vez que necesitemos interactuar con el simulador podemos aprovechar la variable “robot” para enviar un mensaje a la instancia de “Robot” que acabamos de crear. Este objeto nos servirá también para poder obtener los objetos que representan a los distintos dispositivos que posee el robot (motores y sensores).

Incluso más importante que acceder a los dispositivos del robot es el método “step”, que nos permite delegar el control de la ejecución al simulador para que éste lleve a cabo todas las acciones necesarias para avanzar la simulación. 

Si no ejecutamos el método “step” a intervalos regulares, entonces, la simulación no avanza ya que durante la ejecución de “step” el simulador actualiza los valores de los sensores y actuadores además de realizar todos los cálculos de posición, velocidad, y colisiones de cada objeto simulado.

Más información de la función “step” en: [https://cyberbotics.com/doc/guide/controller-programming?tab-language=python#the-step-and-wb_robot_step-functions](https://cyberbotics.com/doc/guide/controller-programming?tab-language=python#the-step-and-wb_robot_step-functions)

Por lo tanto, una vez que tenemos creada nuestra instancia de Robot y podemos mandarle mensajes, el siguiente paso es ejecutar el ciclo de la simulación, usualmente de la siguiente forma:

```python
while robot.step(32) != -1:
    pass # Reemplazar por la lógica del controlador
```

El método “step” espera como argumento un múltiplo de la cantidad de milisegundos que tarda un paso de simulación. El parámetro de la función step especifica la cantidad de tiempo, expresada en milisegundos, que debe simularse hasta que la función step() regrese, es decir, el número de milisegundos entre actualizaciones del mundo. 

Como los pasos de simulación no se pueden interrumpir, la medición de un sensor o el accionamiento de un motor ocurre entre dos pasos de simulación. Debido a eso, por ejemplo, si el paso de simulación es de 16 ms, el argumento que se pasa a robot.step() debe ser un múltiplo de ese valor. Puede ser 16, 32, 64, 128, etc.

Dado que el valor del paso de simulación es una constante que vamos a necesitar más adelante para inicializar los sensores, es recomendable almacenarlo en una variable (usualmente llamada “TIME_STEP”).

Entonces, el código mínimo necesario para programar un controlador válido en webots tiene la siguiente forma:

```python
from controller import Robot

TIME_STEP = 32
robot = Robot()

while robot.step(TIME_STEP) != -1:
    pass # Reemplazar por la lógica del controlador
```

Por supuesto, este código no hace absolutamente nada más que invocar el ciclo de la simulación. Para controlar el robot de forma que tenga algún comportamiento interesante es necesario reemplazar el código dentro del “while” con la lógica que queremos darle al robot.

[Descargar ejemplo completo](ejemplo_1.py)