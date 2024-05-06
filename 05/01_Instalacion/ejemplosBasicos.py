import cv2
import numpy as np

car=cv2.imread('imagenes\\carteles.png')

mitadDeCar=car[:,:410] # selecciona la mitad de la imagen, uso slices para seleccionar una parte de la imagen

carSoloRojo=car.copy() # copia la imagen car
carSoloRojo[:,:,1]=0 # selecciona la segunda componente de la imagen (el verde) y la pone en 0
carSoloRojo[:,:,0]=0 # selecciona la primera componente de la imagen (el azul) y la pone en 0

carSinRojo=car.copy() # copia la imagen car
carSinRojo[:,:,2]=0 # selecciona la tercera componente de la imagen (el rojo) y la pone en 0

carEspejo=cv2.flip(car,1) # invierte la imagen car en el eje horizontal


cv2.imshow('car',car)
cv2.imshow('mitadDeCar',mitadDeCar)
cv2.imshow('carSoloRojo',carSoloRojo)
cv2.imshow('carsinRojo',carSinRojo)
cv2.imshow('carEspejo',carEspejo)

cv2.waitKey(0)
