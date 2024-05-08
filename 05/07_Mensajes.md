# 7. Envío de mensajes al supervisor

**El código que desarrollaremos a continuación está implementado en ContEnvioDemensaje.py**

Una vez que mi o mis funciones me devuelven la letra de la víctima o cartel identificado, si el resultado fue positivo, debemos detener nuestro robot, esperar al menos un segundo en ese estado, y luego enviar un mensaje al supervisor. Con tal objetivo, nuestro robot posee un transmisor llamado emmiter que debemos apuntarlo con una variables como a todos los demás dispositivos.

```python
emitter=robot.getDevice("emitter")
```

Cuando queremos enviar el mensaje, el mecanismo es bastante sencillo, como se puede ver a continuación (y es siempre igual, pueden copiar y pegar este código en cualquiera de los robots que desarrollen):

```python
def enviarMensaje(pos1, pos2, letra):
    let=bytes(letra, 'utf-8') # Convertimos la letra a bytes para poder enviarla en la estructura
    # print("Enviando mensaje con posiciones:", pos1, pos2, let)
    mensaje=struct.pack("i i c", pos1, pos2, let) # estructura el mensaje en el formato correcto
    # print(f"Mensaje: {mensaje}")
    emitter.send(mensaje)

def enviarMensajeVoC(tipo):
    parar()
    delay(1200) # Debemos hacer una pausa antes de enviar el mensaje
    enviarMensaje(int(position["x"]*100), int(position["y"]*100), tipo)
```
Para esto creamos dos funciones:

1. enviarMensaje: es de propósito general, dado que podemos enviar otros mensajes además de los reconocimientos de carteles y víctimas, como pedir un LoP (lack of progress), avisar que se llegó al punto inicial y se desea salir, o simplemente avisar que terminó nuestro recorrido. Recibe de parámetro la posición en x, la posición en y la letra que se desea enviar en el mensaje. Dentro de la función se realizan ciertas conversiones con el método *bytes* y con el método *struct.pack* que formatean el mensaje para ser enviado. Finalmente, con el método *send* del emitter logramos la transmisión.

2. enviarMensajeVoC: es la función específica para mandar el mensaje de la víctima o cartel detectado. Simplemente le pasamos la letra que identifica lo reconocido, y automáticamente calcula la posición (hay que enviarla en cm, por eso lo multiplica por 100), y llama a enviarMensaje con los datos necesarios.

En el ejemplo de código veremos que los envíos están harcodeados, es decir, se realiza el envío en un paso determinado del robot. **Está claro que esto sirve sólo para este código y este mapa. El objetivo es armar la función con lo visto en los pasos anteriores, llamarla en cada movimiento de avance o giro mínimo que se realice, y según lo que retorne, llamar a *enviarMensajeVoC* con la letra correspondiente.**

## EJERCICIO FINAL FINAL!!!!

Implementar todo lo visto en el código del robot.
