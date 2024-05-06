import cv2

vic=cv2.imread('imagenes\\victimas.png') # lee la imagen de la carpeta imagenes
car=cv2.imread('imagenes\\carteles.png') # Idem

cv2.imshow('victimas',vic) # muestra la imagen vic en una ventana de nombre victimas
cv2.imshow('carteles',car) # muestra la imnagen car en una ventana de nombre carteles
cv2.waitKey(0) # espera la pulsación de una tecla para finalizar la ejecución del programa