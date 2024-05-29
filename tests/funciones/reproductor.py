import os
import random
import pygame

# Inicializar pygame mixer
pygame.mixer.init()
# Variable para controlar el estado de reproducción
reproduciendo = False

def mostrar_menu(opciones):
    print('Seleccione una opción:')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')

def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a

def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()

def generar_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()

def menu():
   opciones = {
       '1': ('Pausar Música', pausar),
       '2': ('Reanudar Música', reanudar),
       '3': ('Detener Música', detener)
   }
   generar_menu(opciones, '4')


def reproducir_playlist(playlist_path):
    global reproduciendo
    # Obtener la lista de canciones en la playlist
    songs = [os.path.join(playlist_path, song) for song in os.listdir(playlist_path) if song.endswith('.mp3')]
    if not songs:
        print("No se encontraron archivos MP3 en la playlist.")
        return

    # Reproducir cada canción en la playlist
    for song in songs:
        try:
            print(f"Reproduciendo: {os.path.basename(song)}")
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            reproduciendo = True
            # Esperar a que termine la canción o se detenga la reproducción
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                menu()
                if not reproduciendo:
                    break

        except Exception as e:
            print(f"Error al reproducir {song}: {e}")
            break

def seleccionar_y_reproducir_playlist():
    # Define la ruta de las playlists
    playlists_dir = 'tests\playlist'  # Reemplaza 'ruta/a/tus/playlists' con la ruta real
    playlists = [os.path.join(playlists_dir, playlist) for playlist in os.listdir(playlists_dir) if os.path.isdir(os.path.join(playlists_dir, playlist))]
    if not playlists:
        print("No se encontraron playlists.")
        return

    # Seleccionar una playlist aleatoria
    playlist = random.choice(playlists)
    print(f"Reproduciendo playlist: {os.path.basename(playlist)}")
    reproducir_playlist(playlist)

def pausar():
    if reproduciendo:
        pygame.mixer.music.pause()
        print("Música pausada.")

def reanudar():
    if reproduciendo:
        pygame.mixer.music.unpause()
        print("Música reanudada.")

def detener():
    global reproduciendo
    if reproduciendo:
        pygame.mixer.music.stop()
        reproduciendo = False
        print("Música detenida.")

seleccionar_y_reproducir_playlist()