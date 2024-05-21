from robot import Robot

robot = Robot() 

while robot.step() != -1:
    if not robot.hayAlgoIzquierda():
        robot.girarIzquierda90()
        robot.avanzarBaldosa()
    elif not robot.hayAlgoAdelante():
        robot.avanzarBaldosa()
    elif not robot.hayAlgoDerecha():
        robot.girarDerecha90()
        robot.avanzarBaldosa()
    else:
        robot.girarMediaVuelta()
        robot.avanzarBaldosa()