import cv2

car=cv2.imread('imagenes\\carteles.png')

# cvtColor: Convierte una imagen a otra forma de representación
carGris=cv2.cvtColor(car,cv2.COLOR_BGR2GRAY)

carHSB=cv2.cvtColor(car,cv2.COLOR_BGR2HSV)

carRGBA=cv2.cvtColor(car,cv2.COLOR_BGR2BGRA)

cv2.imshow('carteles',car)
cv2.imshow('cartelesGris',carGris)
cv2.imshow('cartelesHSB',carHSB)
cv2.imshow('cartelesRGBA',carRGBA)

# shape nos muestra el formato de la imagen en alto, ancho y canales (cantidad de bytes por pixel)
print(f"Formato de la imagen en RGB: {car.shape}")
print(f"Formato de la imagen en Gris: {carGris.shape}")
print(f"Formato de la imagen en HSB: {carHSB.shape}")
print(f"Formato de la imagen en RGBA: {carRGBA.shape}")
cv2.waitKey(0)