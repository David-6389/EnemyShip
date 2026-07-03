# recursos.py
import os
import sys
import pygame

pygame.init()

# Caché global para no recargar recursos múltiples veces
_recursos_cacheados = None
musica_actual = None

def cargar_frames_animacion(carpeta, tamanio=None):
    frames = []
    if not os.path.exists(carpeta):
        print(f"No existe la carpeta de animacion: {carpeta}")
        return frames

    archivos = sorted(os.listdir(carpeta))
    for archivo in archivos:
        if archivo.endswith(".png"):
            ruta = os.path.join(carpeta, archivo)
            imagen = pygame.image.load(ruta).convert_alpha()
            if tamanio is not None:
                imagen = pygame.transform.scale(imagen, tamanio)
            frames.append(imagen)
    return frames

def cargar_recursos():
    global _recursos_cacheados
    
    # Si ya se cargaron, devolvemos el caché directamente
    if _recursos_cacheados is not None:
        return _recursos_cacheados

    directorio_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    
    recursos = {
        'imagenes': {
            'fondo': os.path.join(directorio_base, 'image', 'background_space.jpg'),
            'fondo_menu': os.path.join(directorio_base, 'image', 'Background_menu_2.jpg'),
            'plasma': cargar_frames_animacion(os.path.join(directorio_base, 'image', 'plasma'), (25, 25)),
        },
        'sound': {
            'soundtrack_menu': os.path.join(directorio_base, 'sound', 'soundtrack_menu.mp3'),
            'soundtrack_juego': os.path.join(directorio_base, 'sound', 'soundtrack_juego.mp3'),
            'sound_disparo_jugador': os.path.join(directorio_base, 'sound', 'sound_disparo_jugador.mp3'),
            'Disparo_especial_jugador': os.path.join(directorio_base, 'sound', 'Disparo_especial_jugador.mp3'),
            'muerte_jugador': os.path.join(directorio_base, 'sound', 'muerte_jugador.mp3'),
            'sound_Potenciador': os.path.join(directorio_base, 'sound', 'sound_Potenciador.mp3'),
            'colision': os.path.join(directorio_base, 'sound', 'colision.mp3'),
            'sound_disp_Enemigo': os.path.join(directorio_base, 'sound', 'sound_disp_Enemigo.mp3'),
            'Proyectil_especial_Enemy': os.path.join(directorio_base, 'sound', 'Proyectil_especial_Enemy.mp3'),
            'mientras_disp_especial_Enemigo': os.path.join(directorio_base, 'sound', 'mientras_disp_especial_Enemigo.mp3'),
            'Explocion_Enemigo': os.path.join(directorio_base, 'sound', 'Explocion_Enemigo.mp3')
        },
        'font': {
            'font_game': os.path.join(directorio_base, 'font', 'font_menu.TTF')
        }
    }

    for tipo, archivos in recursos.items():
        for nombre, archivo in archivos.items():
            if tipo == 'sound':
                recursos[tipo][nombre] = pygame.mixer.Sound(archivo)
            elif tipo == 'font':
                recursos[tipo][nombre] = pygame.font.Font(archivo, 50)
            else:
                if isinstance(archivo, list):
                    recursos[tipo][nombre] = archivo
                else:
                    recursos[tipo][nombre] = pygame.image.load(archivo).convert()
    
    _recursos_cacheados = recursos
    return _recursos_cacheados

def reproducir_musica(nombre, volumen=0.6):
    global musica_actual
    recursos = cargar_recursos()
    
    if musica_actual == nombre and recursos['sound'][nombre].get_num_channels() > 0:
        return

    detener_musica()
    recursos['sound'][nombre].set_volume(volumen)
    recursos['sound'][nombre].play(loops=-1)
    musica_actual = nombre

def detener_musica():
    global musica_actual
    recursos = cargar_recursos()
    recursos['sound']['soundtrack_menu'].stop()
    recursos['sound']['soundtrack_juego'].stop()
    musica_actual = None