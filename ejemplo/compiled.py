#!/usr/bin/env python
import contextlib as __stickytape_contextlib

@__stickytape_contextlib.contextmanager
def __stickytape_temporary_dir():
    import tempfile
    import shutil
    dir_path = tempfile.mkdtemp()
    try:
        yield dir_path
    finally:
        shutil.rmtree(dir_path)

with __stickytape_temporary_dir() as __stickytape_working_dir:
    def __stickytape_write_module(path, contents):
        import os, os.path

        def make_package(path):
            parts = path.split("/")
            partial_path = __stickytape_working_dir
            for part in parts:
                partial_path = os.path.join(partial_path, part)
                if not os.path.exists(partial_path):
                    os.mkdir(partial_path)
                    with open(os.path.join(partial_path, "__init__.py"), "wb") as f:
                        f.write(b"\n")

        make_package(os.path.dirname(path))

        full_path = os.path.join(__stickytape_working_dir, path)
        with open(full_path, "wb") as module_file:
            module_file.write(contents)

    import sys as __stickytape_sys
    __stickytape_sys.path.insert(0, __stickytape_working_dir)

    __stickytape_write_module('robot.py', b'import math\r\nimport utils\r\nfrom point import Point\r\nfrom controller import Robot as WebotsRobot\r\n\r\nTIME_STEP = 16\r\nMAX_VEL = 3.14 # Reduzco la velocidad para minimizar desv\xc3\xado\r\n\r\nclass Robot:\r\n    def __init__(self):\r\n        self.robot = WebotsRobot()\r\n        \r\n        self.wheelL = self.robot.getDevice("wheel1 motor") \r\n        self.wheelL.setPosition(float("inf"))\r\n\r\n        self.wheelR = self.robot.getDevice("wheel2 motor") \r\n        self.wheelR.setPosition(float("inf"))\r\n\r\n        self.lidar = self.robot.getDevice("lidar")\r\n        self.lidar.enable(TIME_STEP)\r\n\r\n        self.inertialUnit = self.robot.getDevice("inertial_unit")\r\n        self.inertialUnit.enable(TIME_STEP)\r\n\r\n        self.gps = self.robot.getDevice("gps")\r\n        self.gps.enable(TIME_STEP)\r\n\r\n        self.position = None\r\n        self.rotation = 0\r\n        self.rangeImage = None\r\n\r\n        self.wheelL.setVelocity(0)\r\n        self.wheelR.setVelocity(0)\r\n        self.step()\r\n\r\n    def step(self):\r\n        result = self.robot.step(TIME_STEP)\r\n        self.updateVars()\r\n        return result\r\n    \r\n    def updateVars(self):\r\n        self.updatePosition()\r\n        self.updateRotation()\r\n        self.updateRangeImage()\r\n        print(f"Position: {self.position}, Rotation: {self.rotation:.3f} rad ({self.rotation*180/math.pi:.3f} deg)")\r\n    \r\n    def updatePosition(self):\r\n        x, _, y = self.gps.getValues()\r\n        self.position = Point(x, y)\r\n        \r\n    def updateRotation(self):\r\n        _, _, yaw = self.inertialUnit.getRollPitchYaw()\r\n        self.rotation = yaw % math.tau # Normalizamos el valor del \xc3\xa1ngulo (0 a 2*PI)\r\n\r\n    def updateRangeImage(self):\r\n        self.rangeImage = self.lidar.getRangeImage()[1024:1536]\r\n    \r\n    def girar(self, rad):\r\n        lastRot = self.rotation\r\n        deltaRot = 0\r\n\r\n        while self.step() != -1:\r\n            deltaRot += utils.angle_diff(self.rotation, lastRot)\r\n            lastRot = self.rotation\r\n\r\n            diff = utils.angle_diff(deltaRot, abs(rad))\r\n\r\n            mul = (5/math.pi) * diff\r\n            mul = min(max(mul, 0.05), 1)\r\n\r\n            if rad > 0:\r\n                self.wheelL.setVelocity(mul*MAX_VEL)\r\n                self.wheelR.setVelocity(-mul*MAX_VEL)\r\n            else:\r\n                self.wheelL.setVelocity(-mul*MAX_VEL)\r\n                self.wheelR.setVelocity(mul*MAX_VEL)\r\n\r\n            if diff <= 0.005:\r\n                break\r\n\r\n        self.wheelL.setVelocity(0)\r\n        self.wheelR.setVelocity(0)\r\n\r\n    def avanzar(self, distance):\r\n        initPos = self.position\r\n\r\n        while self.step() != -1:\r\n            diff = abs(distance) - initPos.distance_to(self.position)\r\n\r\n            vel = min(max(diff/0.01, 0.1), 1)\r\n            if distance < 0: vel *= -1\r\n            \r\n            self.wheelL.setVelocity(vel*MAX_VEL)\r\n            self.wheelR.setVelocity(vel*MAX_VEL)\r\n\r\n            if diff < 0.001:\r\n                break\r\n        \r\n        self.wheelL.setVelocity(0)\r\n        self.wheelR.setVelocity(0)\r\n        \r\n    def hayAlgoIzquierda(self):\r\n        leftDist = self.rangeImage[128]\r\n        return leftDist < 0.08\r\n\r\n    def hayAlgoDerecha(self):\r\n        rightDist = self.rangeImage[128*3]\r\n        return rightDist < 0.08\r\n\r\n    def hayAlgoAdelante(self):\r\n        frontDist = self.rangeImage[256]\r\n        return frontDist < 0.08\r\n\r\n    def girarIzquierda90(self):\r\n        self.girar(math.tau/4)\r\n\r\n    def girarDerecha90(self):\r\n        self.girar(-math.tau/4)\r\n\r\n    def girarMediaVuelta(self):\r\n        self.girar(math.tau/2)\r\n\r\n    def avanzarBaldosa(self):\r\n        self.avanzar(0.12)')
    __stickytape_write_module('utils.py', b'import math\r\n\r\ndef angle_diff(a, b):\r\n    clockwise = (a - b) % math.tau\r\n    counterclockwise = (b - a) % math.tau\r\n    return min(clockwise, counterclockwise)')
    __stickytape_write_module('point.py', b'import math\r\n\r\nclass Point:\r\n    def __init__(self, x, y):\r\n        self.x = x\r\n        self.y = y\r\n\r\n    def distance_to(self, point):\r\n        dx = self.x-point.x\r\n        dy = self.y-point.y\r\n        return math.sqrt(dx**2 + dy**2)\r\n    \r\n    def __str__(self) -> str:\r\n        return f"({self.x:.3f}, {self.y:.3f})"')
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