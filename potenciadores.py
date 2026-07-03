import math
import random
import pygame
import config as cf
import recursos as rec

recursos = rec.cargar_recursos()

class ScrapPerdido(pygame.sprite.Sprite):  
    def __init__(self, posicion, cantidad):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 255, 0)) # Amarillo brillante
        self.rect = self.image.get_rect(center=posicion)
        self.cantidad = cantidad
    
class Potenciador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        # Círculo del potenciador
        pygame.draw.circle(self.image, cf.CIAN, (10, 10), 10)
        pygame.draw.circle(self.image, cf.BLANCO, (10, 10), 10, 2) # borde blanco

        self.rect = self.image.get_rect()
        # Posición aleatoria en la pantalla
        self.rect.x = random.randrange(cf.ANCHO - self.rect.width)
        self.rect.y = random.randrange(cf.ALTO - self.rect.height)
        self.radio = 1 # Radio del círculo
        self.angulo = random.uniform(0, 2 * math.pi)  # Ángulo inicial

    def update(self):
        self.angulo += 0.1
        self.rect.x =  self.rect.x + self.radio * math.cos(self.angulo)
        self.rect.y = self.rect.y + self.radio * math.sin(self.angulo)

class PotenciadorVida(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        imagen = recursos['imagenes'].get('potenciador_vida')

        if imagen is not None:
            self.image = imagen.copy()
        else:
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)

            # Fondo verde
            pygame.draw.rect(self.image, cf.VERDE, (0, 0, 20, 20), border_radius=10)

            # Cruz blanca
            pygame.draw.rect(self.image, cf.BLANCO, (8, 4, 4, 12), border_radius=2)
            pygame.draw.rect(self.image, cf.BLANCO, (4, 8, 12, 4), border_radius=2)

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(100, cf.ANCHO - 100)
        self.rect.y = random.randint(160, cf.ALTO - 220)
        self.radio = 1
        self.angulo = random.uniform(0, 2 * math.pi)
        self.tiempo_creacion = pygame.time.get_ticks()
        self.duracion = 6000  # dura 6 segundos en pantalla

    def update(self):
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.tiempo_creacion > self.duracion:
            self.kill()

        self.angulo += 0.1
        self.rect.x = self.rect.x + self.radio * math.cos(self.angulo)
        self.rect.y = self.rect.y + self.radio * math.sin(self.angulo)

class Puntos_atributos(pygame.sprite.Sprite):
    def __init__(self, puntos_atributo_nvl_1):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(cf.CIAN)
        self.rect = self.image.get_rect()
        # Posición aleatoria en la pantalla
        self.rect.x = random.randrange(cf.ANCHO - self.rect.width)
        self.rect.y = random.randrange(cf.ALTO - self.rect.height)
        self.radio = 1 # Radio del círculo
        self.angulo = random.uniform(0, 2 * math.pi)  # Ángulo inicial
        self.puntos_atributo_nvl_1 = puntos_atributo_nvl_1 #* 20

    def update(self):
        self.angulo += 0.1
        self.rect.x =  self.rect.x + self.radio * math.cos(self.angulo)
        self.rect.y = self.rect.y + self.radio * math.sin(self.angulo)