import os
import pygame
import pygame.camera
import time

def sacarFoto():
    pygame.camera.init() 
    # Crear una lista de todas las cámaras disponibles
    camlist = pygame.camera.list_cameras() 
    
    # Verificar si hay una cámara disponible
    if camlist: 
        try:
            # Inicializar la variable cam con la cámara predeterminada
            cam = pygame.camera.Camera(camlist[0], (640, 480)) 

            # Abrir la cámara
            cam.start() 

            # Esperar un segundo para permitir que la cámara se inicialice
            time.sleep(1)

            # Capturar una imagen
            image = cam.get_image() 
            
            # Crear la carpeta 'fotos' si no existe
            if not os.path.exists('fotos'):
                os.makedirs('fotos')
            
            # Guardar la imagen en la carpeta 'fotos'
            pygame.image.save(image, os.path.join('fotos', 'filename.jpg')) 
            print("Foto guardada correctamente en la carpeta 'fotos'.")
        
        except Exception as e:
            print(f"Error al capturar o guardar la foto: {e}")
        
        finally:
            # Detener la cámara
            cam.stop()
    
    # Si no se detecta una cámara, ir a la parte del else
    else: 
        print("No camera on current device") 

