import math
import pygame
import config as cf
import recursos as rec
import status_game as sg
from potenciadores import Potenciador

recursos = rec.cargar_recursos()


class Bullet(pygame.sprite.Sprite):
    vidas_perdidas_enemigo = 0

    def __init__(self, position, direction, todos_los_sprites):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(cf.CIAN)
        self.rect = self.image.get_rect()
        # Ajusta la posición inicial de la bala para que salga del borde del jugador
        self.rect.centerx = position[0] + direction.x * 20
        self.rect.centery = position[1] + direction.y * 20
        self.velocity = pygame.math.Vector2(direction.x * 5, direction.y * 5)
        self.todos_los_sprites = todos_los_sprites
        self.todos_los_sprites.add(self)

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        # Elimina la bala si sale de la pantalla
        if not pygame.Rect(0, 0, cf.ANCHO, cf.ALTO).colliderect(self.rect):
            self.kill()

    def colisionar_enemigo(self, grupo_potenciadores, todos_los_sprites):
        self.__class__.vidas_perdidas_enemigo += 1
        print(f"Golpes acumulados para potenciador: {self.__class__.vidas_perdidas_enemigo}")

        if self.__class__.vidas_perdidas_enemigo >= 10:
            potenciador = Potenciador()
            todos_los_sprites.add(potenciador)
            grupo_potenciadores.add(potenciador)
            self.__class__.vidas_perdidas_enemigo = 0


class DisparoEspecial(pygame.sprite.Sprite):
    def __init__(self, jugador, enemigo, todos_los_sprites):
        super().__init__()

        self.frames = recursos['imagenes'].get('plasma', [])
        self.frame_actual = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 2  # 1 = rapido, 2 = normal, 4 = lento

        if self.frames:
            self.image = self.frames[self.frame_actual].copy()
        else:
            self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
            self.image.fill(cf.VIOLETA)

        self.rect = self.image.get_rect()
        self.velocidad = 3
        self.rect.center = jugador.rect.center
        self.jugador = jugador
        self.enemigo = enemigo
        self.todos_los_sprites = todos_los_sprites
        self.todos_los_sprites.add(self)

    def update(self):
        self.animar()

        # Calcula y normaliza la dirección hacia el enemigo
        direccion_x, direccion_y = self.calcular_direccion_hacia_enemigo()
        magnitud = math.sqrt(direccion_x ** 2 + direccion_y ** 2)
        if magnitud != 0:
            direccion_x /= magnitud
            direccion_y /= magnitud

        self.rect.x += self.velocidad * direccion_x
        self.rect.y += self.velocidad * direccion_y

        if not pygame.Rect(0, 0, cf.ANCHO, cf.ALTO).colliderect(self.rect):
            self.kill()

    def animar(self):
        if not self.frames:
            return

        self.contador_animacion += 1

        if self.contador_animacion >= self.velocidad_animacion:
            self.contador_animacion = 0
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)

            centro_anterior = self.rect.center
            self.image = self.frames[self.frame_actual].copy()
            self.rect = self.image.get_rect(center=centro_anterior)

    def calcular_direccion_hacia_enemigo(self):
        dx = self.enemigo.rect.centerx - self.rect.centerx
        dy = self.enemigo.rect.centery - self.rect.centery
        distancia = max(1, math.sqrt(dx ** 2 + dy ** 2))
        direccion_x = dx / distancia
        direccion_y = dy / distancia
        return direccion_x, direccion_y