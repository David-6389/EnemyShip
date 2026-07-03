import os
import math
import pygame
import ui
import config as cf
import recursos as rec
import status_game as sg
from proyectiles import Bullet, DisparoEspecial
from potenciadores import ScrapPerdido

pygame.init()
recursos = rec.cargar_recursos()  # Variable global para almacenar los recursos cargados

class Jugador(pygame.sprite.Sprite):
    def __init__(self, todos_los_sprites):
        super().__init__()
        self.original_image = pygame.image.load("image/nave_player_3.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (90, 90))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (cf.ANCHO/2, cf.ALTO-25)

        self.hitbox = pygame.Rect(0, 0, 28, 28)
        self.hitbox.center = self.rect.center
        
        self.angle = 0
        self.speed_up = cf.VELOCIDAD_AVANCE_JUGADOR
        self.speed_down = 1
        self.speed_sides = cf.VELOCIDAD_GIRO_JUGADOR
        self.vidas = cf.VIDAS_INICIALES_JUGADOR
        self.scrap = cf.SCRAP_INICIAL
        self.experiencia = 0
        self.nivel_jugador = 1
        self.experiencia_siguiente_nivel = 100
        self.puntos_habilidad = 0

        self.escudo_nivel = 0 # 0 = no desbloqueado
        self.escudo_nivel_max = 3
        self.escudo_activo = False
        self.escudo_tiempo_restante = 0
        self.escudo_cooldown_restante = 0

        self.dash_nivel = 0
        self.dash_nivel_max = 3
        self.dash_activo = False
        self.dash_tiempo_restante = 0
        self.dash_cooldown_restante = 0

        self.direction = pygame.math.Vector2(0, -1)
        self.todos_los_sprites = todos_los_sprites
        self.disparos_especial = cf.DISPAROS_ESPECIALES_INICIALES

         # Ajustes visuales para nave de 75x75
        self.propulsor_offset_atras = 32
        self.propulsor_offset_lateral = 21
        self.propulsor_base_offset = 0.45

        # Si el fuego aparece apuntando hacia adelante, cambiá esto a 180
        self.propulsor_rotacion_extra = 0

        # Frames del fuego de los propulsores
        self.propulsor_escala = 0.3
        self.propulsor_frames = self.cargar_frames_propulsor()

        # -1 significa apagado
        self.propulsor_frame_actual = -1

        # Control de velocidad de animación
        self.propulsor_timer = 0
        self.propulsor_delay = 2  # más bajo = más rápido

    def update(self):
        keys = pygame.key.get_pressed()

        avanzando = keys[pygame.K_UP]
        if avanzando:
            self.rect.x += self.direction.x * self.speed_up
            self.rect.y += self.direction.y * self.speed_up

        if keys[pygame.K_DOWN]:
            self.rect.x -= self.direction.x * self.speed_down
            self.rect.y -= self.direction.y * self.speed_down

        if keys[pygame.K_LEFT]:
            self.angle += 2

        if keys[pygame.K_RIGHT]:
            self.angle -= 2

        self.angle %= 360

        if keys[pygame.K_a]:
            self.rect.x -= self.speed_sides * math.cos(math.radians(self.angle))
            self.rect.y += self.speed_sides  * math.sin(math.radians(self.angle))

        if keys[pygame.K_d]:
            self.rect.x += self.speed_sides * math.cos(math.radians(self.angle))
            self.rect.y -= self.speed_sides * math.sin(math.radians(self.angle))

        # Update direction vector based on angle
        self.direction = pygame.math.Vector2(0, -1).rotate(-self.angle)

        self.actualizar_propulsor(avanzando)
        self.actualizar_escudo()
        self.actualizar_dash()

        self.rotate()

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > cf.ANCHO:
            self.rect.right = cf.ANCHO

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > cf.ALTO:
            self.rect.bottom = cf.ALTO

        # La hitbox se sincroniza al final, después de aplicar todo el
        # movimiento del frame (incluido el empuje del dash). Si se hace
        # antes, la hitbox queda un frame atrasada respecto a la nave
        # mientras el dash está activo.
        self.hitbox.center = self.rect.center

    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def dibujar_vidas(self, pantalla):
        CUBO_VIDA = 10
        espacio_entre_cubos = 0
        x = 10
        y = 10
        for _ in range(self.vidas):
            pygame.draw.rect(pantalla, cf.AZUL, (x, y, CUBO_VIDA, CUBO_VIDA))
            x += CUBO_VIDA + espacio_entre_cubos

    def ganar_experiencia(self, cantidad):
        self.experiencia += cantidad
        print(f"Ganaste {cantidad} XP. XP actual: {self.experiencia}/{self.experiencia_siguiente_nivel}")

        while self.experiencia >= self.experiencia_siguiente_nivel:
            self.experiencia -= self.experiencia_siguiente_nivel
            self.nivel_jugador += 1
            self.experiencia_siguiente_nivel = int(self.experiencia_siguiente_nivel * 1.4)

            self.puntos_habilidad += 1

            print(f"SUBISTE A NIVEL {self.nivel_jugador}")
            print(f"Puntos de habilidad disponibles: {self.puntos_habilidad}")

    def dibujar_experiencia(self, pantalla):
        fuente_xp = pygame.font.Font(None, 28)

        texto = fuente_xp.render(
            f"NVL {self.nivel_jugador}  XP {self.experiencia}/{self.experiencia_siguiente_nivel}",
            True,
            cf.BLANCO
        )
        pantalla.blit(texto, (10, 50))

    def perder_vida(self, danio=1):
        if self.escudo_activo:
            print("¡Golpe bloqueado por el escudo!")
            return False
        self.vidas -= danio
        if self.vidas <= 0:
            recursos['sound']['muerte_jugador'].play()
            if self.scrap > 0:
                scrap_perdido = ScrapPerdido(self.rect.center, self.scrap)
                sg.estado_juego.todos_los_sprites.add(scrap_perdido)
                sg.estado_juego.grupo_scrap_perdido.add(scrap_perdido)
                print(f"Scrap perdido al morir: {self.scrap}")
                self.scrap = 0
            print("¡El jugador se quedó sin vidas! Game Over")
            ui.mostrar_mensaje_Game_over()
            return True
        return False

    def dibujar_disparos_especiales(self, pantalla):
        # Dibujar los disparos especiales en pantalla
        x = 10
        y = 30
        for _ in range(self.disparos_especial):
            pygame.draw.rect(pantalla, cf.VIOLETA, (x, y, 10, 10))
            x += 11

    def disparar(self, bullet_group, todos_los_sprites):
        nuevo_proyectil = Bullet(self.rect.center, self.direction, todos_los_sprites)
        todos_los_sprites.add(nuevo_proyectil)
        bullet_group.add(nuevo_proyectil)
        recursos['sound']['sound_disparo_jugador'].play()

    def disparar_especial(self, bullet_especial_group, todos_los_sprites, enemigo):
        if self.disparos_especial > 0:
            nuevo_proyectil_especial = DisparoEspecial(self, enemigo, todos_los_sprites)
            todos_los_sprites.add(nuevo_proyectil_especial)
            bullet_especial_group.add(nuevo_proyectil_especial)
            self.disparos_especial -= 1
            recursos['sound']['Disparo_especial_jugador'].play()
            print(f"disparos especiales = {self.disparos_especial}")
            if self.disparos_especial == 0:
                print("No tienes más disparos especiales! ¡SUERTE ;)")

    def duracion_escudo(self):
        # Nivel 1: 90 frames (~1.5s) | +30 frames por nivel
        return 60 + self.escudo_nivel * 30

    def cooldown_escudo(self):
        # Nivel 1: 360 frames (~6s) | -40 frames por nivel (mínimo 120)
        return max(120, 400 - self.escudo_nivel * 40)

    def activar_escudo(self):
        if self.escudo_nivel <= 0:
            print("No tenés el escudo desbloqueado todavía.")
            return
        if self.escudo_activo or self.escudo_cooldown_restante > 0:
            return  # ya activo o en cooldown

        self.escudo_activo = True
        self.escudo_tiempo_restante = self.duracion_escudo()
        print(f"¡Escudo activado! Nivel {self.escudo_nivel}")

    def actualizar_escudo(self):
        if self.escudo_activo:
            self.escudo_tiempo_restante -= 1
            if self.escudo_tiempo_restante <= 0:
                self.escudo_activo = False
                self.escudo_cooldown_restante = self.cooldown_escudo()
                print("Escudo desactivado, entra en cooldown.")
        elif self.escudo_cooldown_restante > 0:
            self.escudo_cooldown_restante -= 1

    def dibujar_escudo(self, pantalla):
        if self.escudo_activo:
            radio = 55
            superficie = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
            pygame.draw.circle(superficie, (80, 180, 255, 120), (radio, radio), radio)
            pygame.draw.circle(superficie, (150, 220, 255, 200), (radio, radio), radio, 3)
            pantalla.blit(superficie, (self.rect.centerx - radio, self.rect.centery - radio))
    
    def dibujar_estado_escudo(self, pantalla):
                if self.escudo_nivel <= 0:
                    return
                fuente = pygame.font.Font(None, 24)
                if self.escudo_activo:
                    texto = f"ESCUDO ACTIVO ({self.escudo_tiempo_restante // 60 + 1}s)"
                    color = (150, 220, 255)
                elif self.escudo_cooldown_restante > 0:
                    texto = f"Escudo: {self.escudo_cooldown_restante // 60 + 1}s"
                    color = (150, 150, 150)
                else:
                    texto = "Escudo: LISTO (Shift)"
                    color = (255, 255, 255)
                render = fuente.render(texto, True, color)
                pantalla.blit(render, (10, 80))

    def duracion_dash(self):
        # Nivel 1: 12 frames de impulso | +4 frames por nivel
        return 12 + self.dash_nivel * 4

    def cooldown_dash(self):
        # Nivel 1: 200 frames (~3.3s) | -30 por nivel (mínimo 80)
        return max(80, 200 - self.dash_nivel * 30)

    def velocidad_dash(self):
        # Nivel 1: +6 extra de velocidad | +1.5 por nivel
        return 6 + self.dash_nivel * 1.5

    def activar_dash(self):
        if self.dash_nivel <= 0:
            print("No tenés el dash desbloqueado todavía.")
            return
        if self.dash_activo or self.dash_cooldown_restante > 0:
            return

        self.dash_activo = True
        self.dash_tiempo_restante = self.duracion_dash()
        print(f"¡Dash activado! Nivel {self.dash_nivel}")

    def actualizar_dash(self):
        if self.dash_activo:
            # Empuja al jugador en la dirección hacia la que está apuntando
            self.rect.x += self.direction.x * self.velocidad_dash()
            self.rect.y += self.direction.y * self.velocidad_dash()

            self.dash_tiempo_restante -= 1
            if self.dash_tiempo_restante <= 0:
                self.dash_activo = False
                self.dash_cooldown_restante = self.cooldown_dash()
                print("Dash terminado, entra en cooldown.")
        elif self.dash_cooldown_restante > 0:
            self.dash_cooldown_restante -= 1

    def dibujar_estado_dash(self, pantalla):
        if self.dash_nivel <= 0:
            return
        fuente = pygame.font.Font(None, 24)
        if self.dash_activo:
            texto = "DASH!"
            color = (255, 200, 60)
        elif self.dash_cooldown_restante > 0:
            texto = f"Dash: {self.dash_cooldown_restante // 60 + 1}s"
            color = (150, 150, 150)
        else:
            texto = "Dash: LISTO (E)"
            color = (255, 255, 255)
        render = fuente.render(texto, True, color)
        pantalla.blit(render, (10, 105))

    def cargar_frames_propulsor(self):
        frames = []

        for i in range(1, 16):
            ruta = os.path.join(
                "image",
                "fuego_propulsor",
                f"fuego_propulsor{i:02}.png"
            )

            imagen = pygame.image.load(ruta).convert_alpha()
            ancho_original = imagen.get_width()
            alto_original = imagen.get_height()

            nuevo_ancho = int(ancho_original * self.propulsor_escala)
            nuevo_alto = int(alto_original * self.propulsor_escala)

            imagen = pygame.transform.smoothscale(imagen, (nuevo_ancho, nuevo_alto))

            frames.append(imagen)

        return frames
    
    def actualizar_propulsor(self, avanzando):
        self.propulsor_timer += 1

        if self.propulsor_timer < self.propulsor_delay:
            return

        self.propulsor_timer = 0

        if avanzando:
            # Si está apagado, arranca en fuego_propulsor01
            if self.propulsor_frame_actual == -1:
                self.propulsor_frame_actual = 0

            # Crece desde fuego_propulsor01 hasta fuego_propulsor11
            elif self.propulsor_frame_actual < 10:
                self.propulsor_frame_actual += 1

            # Después de fuego_propulsor11 pasa a fuego_propulsor12
            elif self.propulsor_frame_actual == 10:
                self.propulsor_frame_actual = 11

            # Mantiene loop entre fuego_propulsor12 y fuego_propulsor15
            else:
                self.propulsor_frame_actual += 1

                if self.propulsor_frame_actual > 14:
                    self.propulsor_frame_actual = 11

        else:
            # Si soltás UP, decrece desde donde esté hasta apagarse
            if self.propulsor_frame_actual > 0:
                self.propulsor_frame_actual -= 1
            else:
                self.propulsor_frame_actual = -1

    def dibujar_propulsores(self, pantalla):
        if self.propulsor_frame_actual < 0:
            return

        frame = self.propulsor_frames[self.propulsor_frame_actual]

        frame_rotado = pygame.transform.rotate(
            frame,
            self.angle + self.propulsor_rotacion_extra
        )

        centro_nave = pygame.math.Vector2(self.rect.center)

        # Dirección hacia atrás de la nave
        atras = -self.direction

        # Dirección lateral según la rotación de la nave
        derecha = pygame.math.Vector2(1, 0).rotate(-self.angle)

        posicion_izquierda = (
            centro_nave
            + atras * self.propulsor_offset_atras
            - derecha * self.propulsor_offset_lateral
        )

        posicion_derecha = (
            centro_nave
            + atras * self.propulsor_offset_atras
            + derecha * self.propulsor_offset_lateral
        )

        for posicion_base in [posicion_izquierda, posicion_derecha]:
            # IMPORTANTE:
            # usar frame.get_height(), no frame_rotado.get_height()
            # porque frame_rotado cambia su caja al rotar
            desplazamiento_base = atras * (frame.get_height() * self.propulsor_base_offset)

            centro_fuego = pygame.math.Vector2(posicion_base) + desplazamiento_base

            rect_fuego = frame_rotado.get_rect(
                center=(round(centro_fuego.x), round(centro_fuego.y))
            )

            pantalla.blit(frame_rotado, rect_fuego)