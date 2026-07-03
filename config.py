import pygame

pygame.init()

# ============================================================
#  PANTALLA
# ============================================================
info = pygame.display.Info()
ANCHO = info.current_w
ALTO = info.current_h
PANTALLA = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("Enemy Ship")

# ============================================================
#  COLORES
# ============================================================
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
CIAN = (16, 193, 185)
VIOLETA = (183, 70, 228)
GAME_OVER = (0, 0, 0, 220)

# ============================================================
#  BALANCE - JUGADOR
# ============================================================
VIDAS_INICIALES_JUGADOR = 5
DISPAROS_ESPECIALES_INICIALES = 4
VELOCIDAD_AVANCE_JUGADOR = 4
VELOCIDAD_GIRO_JUGADOR = 3
SCRAP_INICIAL = 0
DANIO_DISPARO_NORMAL = 1
DANIO_DISPARO_ESPECIAL = 2