import pygame
import random
import math
import sys
import os
from niveles import NIVELES, generar_ola
#from enemigos import Enemigo, EnemigoKamikaze, EnemigoTorreta

pygame.init()
import menu

#*dimensiones de la pantalla
ANCHO = 1080
ALTO = 720
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Nave Invasora")

#* colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
CIAN = (16, 193, 185)
VIOLETA = (183, 70, 228)
GAME_OVER = (0, 0, 0, 220)

# ... (colores)

#* Atributos del Jugador
VIDAS_INICIALES_JUGADOR = 5
DISPAROS_ESPECIALES_INICIALES = 4
VELOCIDAD_AVANCE_JUGADOR = 4
VELOCIDAD_GIRO_JUGADOR = 3
SCRAP_INICIAL = 0
DANIO_DISPARO_NORMAL = 1
DANIO_DISPARO_ESPECIAL = 2

#* Atributos del Enemigo
VIDAS_INICIALES_ENEMIGO = 1 #! Ajustar según nivel
COOLDOWN_DISPARO_ENEMIGO = 60 # en frames

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

    print(f"Frames cargados desde {carpeta}: {len(frames)}")
    return frames


# carga de sounds e imagenes
def cargar_recursos():
    directorio_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    
    recursos = {
        'imagenes': {
            'fondo': os.path.join(directorio_base, 'image', 'background_space.jpg'),
        
            'plasma': cargar_frames_animacion(
                os.path.join(directorio_base, 'image', 'plasma'),
                (25, 25)
            ),
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
    return recursos

recursos = cargar_recursos()

musica_actual = None

def reproducir_musica(nombre, volumen=0.6):
    global musica_actual

    # Si ya está sonando esa música, no la vuelvas a iniciar
    if musica_actual == nombre and recursos['sound'][nombre].get_num_channels() > 0:
        return

    # Frenar todas las músicas de fondo
    recursos['sound']['soundtrack_menu'].stop()
    recursos['sound']['soundtrack_juego'].stop()

    recursos['sound'][nombre].set_volume(volumen)
    recursos['sound'][nombre].play(loops=-1)

    musica_actual = nombre


def detener_musica():
    global musica_actual

    recursos['sound']['soundtrack_menu'].stop()
    recursos['sound']['soundtrack_juego'].stop()

    musica_actual = None


# Cargar imagen de fondo
fondo = recursos['imagenes']['fondo']
fondo_rect = fondo.get_rect()
fondo_y = 0  # Coordenada y inicial del fondo

font_game = recursos['font']['font_game']

# jugador_img = recursos['imagenes']['image_jugador']
# jugador = jugador_img.get_rect()

#* cargar imágenes
def cargar_imagen(ruta):
    return pygame.image.load(ruta).convert_alpha()

#? GAME OVER
def mostrar_mensaje_Game_over():
    # Superponer un rectángulo semitransparente sobre toda la pantalla
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill(GAME_OVER)
    PANTALLA.blit(overlay, (0, 0))

    texto = font_game.render("GAME OVER", True, BLANCO)
    PANTALLA.blit(texto, ((ANCHO - texto.get_width()) // 2, (ALTO - texto.get_height()) // 2))
    pygame.display.flip()
    pygame.time.delay(2000)


#? WINNER
def mostrar_mensaje_WIN():
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill(GAME_OVER)
    PANTALLA.blit(overlay, (0, 0))

    texto_inicial = font_game.render("GANASTE !!!", True, BLANCO)
    PANTALLA.blit(texto_inicial, ((ANCHO - texto_inicial.get_width()) // 2, (ALTO - texto_inicial.get_height()) // 2))
    pygame.display.flip()
    pygame.time.delay(1000)

    texto_final = font_game.render("CONTINUARA...", True, BLANCO)
    PANTALLA.blit(texto_final, ((ANCHO - texto_final.get_width()) // 2, (ALTO - texto_final.get_height()) // 1.7))
    pygame.display.flip()
    pygame.time.delay(2500)


#! CLASES
class Jugador(pygame.sprite.Sprite):
    def __init__(self, todos_los_sprites):
        super().__init__()
        self.original_image = pygame.image.load("image/nave_player_3.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (90, 90))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO/2, ALTO-25)

        self.hitbox = pygame.Rect(0, 0, 28, 28)
        self.hitbox.center = self.rect.center
        
        self.angle = 0
        self.speed_up = VELOCIDAD_AVANCE_JUGADOR
        self.speed_down = 1
        self.speed_sides = VELOCIDAD_GIRO_JUGADOR
        self.vidas = VIDAS_INICIALES_JUGADOR
        self.scrap = SCRAP_INICIAL
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
        self.disparos_especial = DISPAROS_ESPECIALES_INICIALES
        self.disparos_especiales_image = pygame.Surface((10, 10))

         # Ajustes visuales para nave de 75x75
        #self.propulsor_tamanio = (14, 26)
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

        # Cuando ya está prendido, queda animando entre estos frames: 12, 13, 14 y 15
        self.propulsor_loop_frames = [11, 12, 13, 14]  # índices reales: frame12 a frame15
        self.propulsor_loop_pos = 0

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
        self.hitbox.center = self.rect.center

        self.actualizar_propulsor(avanzando)
        self.actualizar_escudo()
        self.actualizar_dash()

        self.rotate()

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > ANCHO:
            self.rect.right = ANCHO

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def dibujar_vidas(self, pantalla):
        CUBO_VIDA = 10
        espacio_entre_cubos = 0
        x = 10
        y = 10
        for _ in range(self.vidas):
            pygame.draw.rect(pantalla, AZUL, (x, y, CUBO_VIDA, CUBO_VIDA))
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
            BLANCO
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
                todos_los_sprites.add(scrap_perdido)
                grupo_scrap_perdido.add(scrap_perdido)
                print(f"Scrap perdido al morir: {self.scrap}")
                self.scrap = 0
            # sound_muerte_Judagor.play()
            print("¡El jugador se quedó sin vidas! Game Over")
            mostrar_mensaje_Game_over()
            return True
        return False
    
    def perder_vida_es(self):
        if self.escudo_activo:
            print("¡Golpe bloqueado por el escudo!")
            return False
        self.vidas -= 1
        if self.vidas <= 0:
            recursos['sound']['muerte_jugador'].play()
            if self.scrap > 0:
                scrap_perdido = ScrapPerdido(self.rect.center, self.scrap)
                todos_los_sprites.add(scrap_perdido)
                grupo_scrap_perdido.add(scrap_perdido)
                print(f"Scrap perdido al morir: {self.scrap}")
                self.scrap = 0
            # sound_muerte_Judagor.play()
            print("¡El jugador se quedó sin vidas! Game Over")
            mostrar_mensaje_Game_over()
            return True
        return False

    def dibujar_disparos_especiales(self, pantalla):
        # Dibujar los disparos especiales en pantalla
        x = 10
        y = 30
        for _ in range(self.disparos_especial):
            pygame.draw.rect(pantalla, VIOLETA, (x, y, 10, 10))
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

class ScrapPerdido(pygame.sprite.Sprite):
    def __init__(self, posicion, cantidad):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 255, 0)) # Amarillo brillante
        self.rect = self.image.get_rect(center=posicion)
        self.cantidad = cantidad

class Bullet(pygame.sprite.Sprite):
    vidas_perdidas_enemigo = 0
    def __init__(self, position, direction, todos_los_sprites):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(CIAN)
        self.rect = self.image.get_rect()
         # Ajusta la posición inicial de la bala para que salga del borde del jugador
        self.rect.centerx = position[0] + direction.x * 20  # Ajusta 25 según el tamaño del jugador
        self.rect.centery = position[1] + direction.y * 20  # Ajusta 25 según el tamaño del jugador
        self.velocity = pygame.math.Vector2(direction.x * 5, direction.y * 5)
        self.todos_los_sprites = todos_los_sprites
        self.todos_los_sprites.add(self)

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        # Elimina la bala si sale de la pantalla
        if not pygame.Rect(0, 0, ANCHO, ALTO).colliderect(self.rect):
            self.kill()

    def colisionar_enemigo(self):
        self.__class__.vidas_perdidas_enemigo += 1
        print(f"ESTOY DENTRO DE COLISIONAR ENEMIGO --------> {self.__class__.vidas_perdidas_enemigo}")
        if  self.__class__.vidas_perdidas_enemigo >= 10:  # Por ejemplo, cuando el proyectil hace perder 10 vidas al enemigo
            potenciador = Potenciador()
            todos_los_sprites.add(potenciador)
            grupo_potenciadores.add(potenciador)
            self.__class__.vidas_perdidas_enemigo = 0

    def disparar_normal(self, bullet_group, todos_los_sprites, recursos):
        if not self.bullet_fired:
            nuevo_proyectil = Bullet(self.rect.center, self.direction, todos_los_sprites)
            todos_los_sprites.add(nuevo_proyectil)
            bullet_group.add(nuevo_proyectil)
            recursos['sound']['sound_disparo_jugador'].play()
            self.bullet_fired = True


class DisparoEspecial(pygame.sprite.Sprite):
    def __init__(self, jugador, enemigo, todos_los_sprites):
        super().__init__()

        self.frames = recursos['imagenes'].get('plasma', [])
        print("FRAMES PLASMA EN DISPARO ESPECIAL:", len(self.frames))
        self.frame_actual = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 2  # 1 = rapido, 2 = normal, 4 = lento

        if self.frames:
            self.image = self.frames[self.frame_actual].copy()
        else:
            self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
            self.image.fill(VIOLETA)
        #self.image = pygame.Surface((10, 10))
        #self.image.fill(VIOLETA)
        self.rect = self.image.get_rect()
        self.velocidad = 3
        self.rect.center = jugador.rect.center
        self.jugador = jugador
        self.enemigo = enemigo
        self.todos_los_sprites = todos_los_sprites
        self.todos_los_sprites.add(self)

    def update(self):
        self.animar()

        # Calcula la dirección hacia el enemigo
        direccion_x, direccion_y = self.calcular_direccion_hacia_enemigo()
        # Normaliza la dirección para asegurarse de que sea un vector unitario
        magnitud = math.sqrt(direccion_x ** 2 + direccion_y ** 2)
        if magnitud != 0:
            direccion_x /= magnitud
            direccion_y /= magnitud
        # Mueve el disparo en esa dirección
        self.rect.x += self.velocidad * direccion_x
        self.rect.y += self.velocidad * direccion_y
        # Eliminar el disparo especial si sale de la pantalla
        if not pygame.Rect(0, 0, ANCHO, ALTO).colliderect(self.rect):
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
    
    # def disparar_especial(self, bullet_especial_group, todos_los_sprites, recursos):
    #     if jugador.disparos_especial > 0:
    #         nuevo_proyectil_especial = DisparoEspecial(self.jugador, self.enemigo, todos_los_sprites)
    #         todos_los_sprites.add(nuevo_proyectil_especial)
    #         bullet_especial_group.add(nuevo_proyectil_especial)
    #         jugador.disparos_especial -= 1
    #         recursos['sound']['Disparo_especial_jugador'].play()
    #         print(f"disparos especiales = {jugador.disparos_especial}")
    #         if jugador.disparos_especial == 0:
    #             print("No tienes más disparos especiales! ¡SUERTE ;)")


class Potenciador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        # Círculo del potenciador
        pygame.draw.circle(self.image, CIAN, (10, 10), 10)
        pygame.draw.circle(self.image, BLANCO, (10, 10), 10, 2) # borde blanco

        self.rect = self.image.get_rect()
        # Posición aleatoria en la pantalla
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(ALTO - self.rect.height)
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
            pygame.draw.rect(self.image, VERDE, (0, 0, 20, 20), border_radius=10)

            # Cruz blanca
            pygame.draw.rect(self.image, BLANCO, (8, 4, 4, 12), border_radius=2)
            pygame.draw.rect(self.image, BLANCO, (4, 8, 12, 4), border_radius=2)

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(100, ANCHO - 100)
        self.rect.y = random.randint(160, ALTO - 220)
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
        self.image.fill(CIAN)
        self.rect = self.image.get_rect()
        # Posición aleatoria en la pantalla
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(ALTO - self.rect.height)
        self.radio = 1 # Radio del círculo
        self.angulo = random.uniform(0, 2 * math.pi)  # Ángulo inicial
        self.puntos_atributo_nvl_1 = puntos_atributo_nvl_1 #* 20

    def update(self):
        self.angulo += 0.1
        self.rect.x =  self.rect.x + self.radio * math.cos(self.angulo)
        self.rect.y = self.rect.y + self.radio * math.sin(self.angulo)

class ProyectilEnemigo(pygame.sprite.Sprite):
    def __init__(self, posicion, direccion_x, direccion_y, sigue_jugador = False):
        super().__init__()
        if sigue_jugador:
            self.image = pygame.Surface((9, 9))
            self.image.fill(VERDE)
            self.velocidad = 1.5  # Velocidad más lenta
        else:
            self.image = pygame.Surface((5, 5))
            self.image.fill(ROJO)
            self.velocidad = 4  # Velocidad normal
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        self.direccion_x = direccion_x
        self.direccion_y = direccion_y
        self.sigue_jugador = sigue_jugador
        self.sound_played_esp = False
        self.sound_played = False
        
    def update(self):
        if self.sigue_jugador:
            # Si el proyectil sigue al jugador, actualizar su dirección
            dx = jugador.rect.centerx - self.rect.centerx
            dy = jugador.rect.centery - self.rect.centery
            distancia = math.sqrt(dx ** 2 + dy ** 2)
            if not self.sound_played_esp:
                recursos['sound']['Proyectil_especial_Enemy'].play() #* --> sound disparo Especial
                self.sound_played_esp = True
                self.sound_played = False
            if distancia != 0:
                self.direccion_x = dx / distancia
                self.direccion_y = dy / distancia
        else:
            if not self.sound_played and not self.sound_played_esp:
                recursos['sound']['sound_disp_Enemigo'].play() #* --> sound disparo Normal
                self.sound_played = True
        # else:
            # print("NO ESTA DENTRO DE PROYECTIL SEGUIDOR")
        self.rect.x += self.velocidad * self.direccion_x
        self.rect.y += self.velocidad * self.direccion_y

        if not pygame.Rect(0, 0, ANCHO, ALTO).colliderect(self.rect):
            self.kill()


def reiniciar_juego():
    print()
    print("|------- REINICIAR -------|") 
    # Restablecer los atributos del jugador
    jugador.rect.center = (ANCHO / 2, ALTO - 25)
    jugador.vidas = VIDAS_INICIALES_JUGADOR
    jugador.disparos_especial = DISPAROS_ESPECIALES_INICIALES
    jugador.angle = 0
    
    # Vaciar todos los grupos de sprites excepto el jugador
    todos_los_sprites.empty()
    todos_los_sprites.add(jugador)

    enemigos.empty()
    bullet.empty()
    bullet_especial.empty()
    proyectiles_enemigos.empty()
    lista_sprites_puntos_atributos.empty()
    grupo_potenciadores.empty()
    grupo_potenciadores_vida.empty()
    grupo_scrap_perdido.empty()

pygame.font.init()

flash_tiempo = 0
FLASH_DURACION = 1


# Crear grupos de sprites
todos_los_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
proyectiles_enemigos = pygame.sprite.Group()
bullet = pygame.sprite.Group()
bullet_especial = pygame.sprite.Group()
grupo_potenciadores = pygame.sprite.Group()
lista_sprites_puntos_atributos = pygame.sprite.Group()
grupo_scrap_perdido = pygame.sprite.Group()
grupo_potenciadores_vida = pygame.sprite.Group()

# Instancias
jugador = Jugador(todos_los_sprites)
todos_los_sprites.add(jugador)
potenciador = None

def colision_hitbox_jugador(jugador_sprite, otro_sprite):
    return jugador_sprite.hitbox.colliderect(otro_sprite.rect)

#! BUCLE PRINCIPAL
def main():
    jugador_ganador = False
    clock = pygame.time.Clock()
    mostrando_controles = False
    track_menu_play = False
    jugando = True
    en_menu = True
    opcion_seleccionada = 1
    fondo_y = 0
    flash_tiempo = 0
    
    # --- ¡NUEVO! Control de niveles y olas ---
    nivel_actual = 0
    ola_actual = 0
    esperando_siguiente_ola = False
    tiempo_inicio_espera_ola = 0
    DELAY_ENTRE_OLAS = 5000  # 5 segundos
    #generar_ola(nivel_actual, ola_actual, jugador, enemigos, todos_los_sprites, proyectiles_enemigos, recursos)
    # -----------------------------------------

    while jugando:
        reproducir_musica('soundtrack_menu', 0.6)
        bullet_fired = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            elif evento.type == pygame.KEYDOWN:
                if en_menu:
                    if evento.key == pygame.K_RETURN:
                        if opcion_seleccionada == 1:  # Jugar
                            en_menu = False
                            mostrando_controles = False
                            reproducir_musica('soundtrack_juego', 0.6)
                            track_menu_play = False

                        # limpiar por las dudas
                            enemigos.empty()
                            proyectiles_enemigos.empty()
                            bullet.empty()
                            bullet_especial.empty()
                            todos_los_sprites.empty()
                            todos_los_sprites.add(jugador)

                            nivel_actual = 0
                            ola_actual = 0
                            generar_ola(
                                nivel_actual,
                                ola_actual,
                                jugador,
                                enemigos,
                                todos_los_sprites,
                                proyectiles_enemigos,
                                recursos
                            )
                            print("Cantidad enemigos:", len(enemigos))
                            print("Cantidad sprites:", len(todos_los_sprites))

                        elif opcion_seleccionada == 2:  # Controles
                            print(f"en RETURN: {track_menu_play}")
                            track_menu_play = True
                            en_menu = False
                            mostrando_controles = True
                        elif opcion_seleccionada == 3:  # Salir
                            jugando = False
                    elif evento.key == pygame.K_UP:
                        if opcion_seleccionada == 1:
                            opcion_seleccionada = 3
                        else:
                            opcion_seleccionada = max(1, opcion_seleccionada - 1)
                    elif evento.key == pygame.K_DOWN:
                        if opcion_seleccionada == 3:
                            opcion_seleccionada = 1
                        else:
                            opcion_seleccionada = min(3, opcion_seleccionada + 1)
                else:
                    if evento.key == pygame.K_i:
                        menu.mostrar_menu_mejoras(PANTALLA, jugador)
                    elif evento.key == pygame.K_c:
                        jugador.activar_escudo()
                    elif evento.key == pygame.K_LSHIFT:
                        jugador.activar_dash()
                    elif evento.key == pygame.K_SPACE and not bullet_fired:  # Verifica si se presionó la tecla de espacio y no se ha disparado un proyectil
                        jugador.disparar(bullet, todos_los_sprites)
                        bullet_fired = True
                        
                    elif evento.key == pygame.K_LCTRL:
                        # El disparo especial necesita un objetivo, apuntamos al primer enemigo de la lista
                        if enemigos:
                            enemigo_objetivo = enemigos.sprites()[0]
                            jugador.disparar_especial(bullet_especial, todos_los_sprites, enemigo_objetivo)

                    elif evento.key == pygame.K_ESCAPE:  # Regresar al menú desde los controles
                        en_menu = True
                        mostrando_controles = False
                        print(f"en SCAPE: {track_menu_play}")
                        if not track_menu_play:
                            detener_musica()
                            reproducir_musica('soundtrack_menu', 0.6)
                            track_menu_play = True
        #! Renderizado
        if en_menu:
            menu.mostrar_menu(PANTALLA, opcion_seleccionada)
        elif mostrando_controles:
            menu.mostrar_controles(PANTALLA)
        else:
            todos_los_sprites.update()

            # Mover el fondo hacia arriba
            fondo_y -= 1
            if fondo_y <= -fondo_rect.height:
                fondo_y = 0

            #bullet.update()
            #proyectiles_enemigos.update()
            
            #* Colisión: proyectiles enemigos contra jugador
            if pygame.sprite.spritecollide(jugador, proyectiles_enemigos, True, colision_hitbox_jugador):
                flash_tiempo = FLASH_DURACION
                flash_color = BLANCO
                recursos['sound']['colision'].play()

                jugador_muerto = jugador.perder_vida(DANIO_DISPARO_NORMAL)

                print("¡El jugador ha sido golpeado! Vidas restantes:", jugador.vidas)

                if jugador_muerto:
                    detener_musica()
                    reproducir_musica('soundtrack_menu', 0.6)
                    reiniciar_juego()

                    en_menu = True
                    mostrando_controles = False
                    esperando_siguiente_ola = False
                    tiempo_inicio_espera_ola = 0

            #* Colisión: enemigos contra jugador, especialemente para enemigos kamikaze
            colision_enemigo_jugador = pygame.sprite.spritecollide(jugador, enemigos, False, colision_hitbox_jugador)
            jugador_muerto_por_contacto = False
            
            for enemigo_contacto in colision_enemigo_jugador:

                danio = getattr(enemigo_contacto, "danio_contacto", 0)

                if danio > 0:
                    flash_tiempo = FLASH_DURACION
                    flash_color = ROJO
                    recursos['sound']['colision'].play()

                    for _ in range(danio):
                        jugador_muerto_por_contacto = jugador.perder_vida(DANIO_DISPARO_NORMAL)

                    print("¡El jugador chocó con un enemigo! Vidas restantes:", jugador.vidas)

                    if getattr(enemigo_contacto, "morir_al_chocar", False):
                        enemigo_contacto.kill()

                    if jugador_muerto_por_contacto:
                        break

            if jugador_muerto_por_contacto:
                detener_musica()
                reproducir_musica('soundtrack_menu', 0.6)

                reiniciar_juego()

                en_menu = True
                mostrando_controles = False
                esperando_siguiente_ola = False
                tiempo_inicio_espera_ola = 0

            #* Colisión: balas normales contra enemigos
            impactos_enemigos = pygame.sprite.groupcollide(bullet, enemigos, False, False)

            for proyectil, enemigos_afectados in impactos_enemigos.items():
                for enemigo_afectado in enemigos_afectados:
                    murio_enemigo = enemigo_afectado.perder_vida(DANIO_DISPARO_NORMAL)

                    recursos['sound']['colision'].play()
                    proyectil.kill()
                    proyectil.colisionar_enemigo()

                    print("¡Enemigo golpeado! VIDAS RESTANTES:", enemigo_afectado.vidas)

                    if murio_enemigo:
                        xp_ganada = getattr(enemigo_afectado, "xp", 10)
                        jugador.ganar_experiencia(xp_ganada)
                        print(f"Enemigo destruido. Ganaste {xp_ganada} XP")


            #* Colisión: disparos especiales contra enemigos
            impactos_especiales_enemigos = pygame.sprite.groupcollide(bullet_especial, enemigos, True, False)

            for proyectil_especial, enemigos_afectados in impactos_especiales_enemigos.items():
                for enemigo_afectado in enemigos_afectados:
                    murio_enemigo = enemigo_afectado.perder_vida(DANIO_DISPARO_ESPECIAL)

                    recursos['sound']['colision'].play()
                    print("¡Enemigo golpeado con disparo especial! VIDAS RESTANTES:", enemigo_afectado.vidas)

                    if murio_enemigo:
                        xp_ganada = getattr(enemigo_afectado, "xp", 10)
                        jugador.ganar_experiencia(xp_ganada)
                        print(f"Enemigo destruido con disparo especial. Ganaste {xp_ganada} XP")


            # Control de fin de oleada
            if not enemigos and not en_menu and not esperando_siguiente_ola:
                esperando_siguiente_ola = True
                tiempo_inicio_espera_ola = pygame.time.get_ticks()
                print("Ola terminada. Preparando siguiente ola...")

                 # Potenciador de vida entre oleadas
                chance = random.random()

                if chance < 0.99:
                    potenciador_vida = PotenciadorVida()
                    todos_los_sprites.add(potenciador_vida)
                    grupo_potenciadores_vida.add(potenciador_vida)
                    print("Apareció un potenciador de vida")

                # 20% restante: abrir menú de mejoras si el jugador tiene puntos
                elif jugador.puntos_habilidad > 0:
                    print("Tenés puntos de habilidad disponibles")
                    menu.mostrar_menu_mejoras(PANTALLA, jugador)                  
  
            # Crear siguiente oleada después del delay
            if esperando_siguiente_ola:
                tiempo_actual = pygame.time.get_ticks()

                if tiempo_actual - tiempo_inicio_espera_ola >= DELAY_ENTRE_OLAS:
                    esperando_siguiente_ola = False

                    ola_actual += 1

                    if ola_actual >= len(NIVELES[nivel_actual]["olas"]):
                        nivel_actual += 1
                        ola_actual = 0

                    if not generar_ola(
                        nivel_actual,
                        ola_actual,
                        jugador,
                        enemigos,
                        todos_los_sprites,
                        proyectiles_enemigos,
                        recursos
                    ):
                        en_menu = True

            #* colisiones entre Proyectiles
            colisiones_proyectiles = pygame.sprite.groupcollide(bullet, proyectiles_enemigos, True, True)
            for _ in colisiones_proyectiles.values():
                for proyectil_enemigo in _:
                    proyectil_enemigo.kill()
    
            
            #* colisiones entre Proyectiles_especiales
            colisiones_proyectiles_especiales = pygame.sprite.groupcollide(bullet_especial, proyectiles_enemigos, True, True)
            for _ in colisiones_proyectiles_especiales.values():
                for proyectil_enemigo in _:
                    proyectil_enemigo.kill()

            colision_scrap = pygame.sprite.spritecollide(jugador, grupo_scrap_perdido, True)
            for scrap_recuperado in colision_scrap:
                jugador.scrap += scrap_recuperado.cantidad
                print(f"¡Scrap recuperado! Tienes {jugador.scrap} de scrap.")
                recursos['sound']['sound_Potenciador'].play() # cambiarlo porque es el mismo sonido que el potenciador       

            #* Agarrar potenciador de disparos especiales
            colisiones_potenciador = pygame.sprite.spritecollide(jugador, grupo_potenciadores, True)
            for _ in colisiones_potenciador:
                recursos['sound']['sound_Potenciador'].play()
                jugador.disparos_especial += 3 #! agrega tres disparos especiales

            #* Agarrar potenciador de vida
            colisiones_vida = pygame.sprite.spritecollide(jugador, grupo_potenciadores_vida, True)
            for _ in colisiones_vida:
                jugador.vidas += 1
                recursos['sound']['sound_Potenciador'].play()
                print("¡Potenciador de vida tomado! Vidas actuales:", jugador.vidas)
                
            if flash_tiempo > 0:
                PANTALLA.fill(flash_color)
                flash_tiempo -= 1
            else:
                PANTALLA.blit(fondo, (0, fondo_y))
                PANTALLA.blit(fondo, (0, fondo_y + fondo_rect.height))
                PANTALLA.fill(NEGRO, special_flags=pygame.BLEND_RGB_ADD)

            # Primero el fuego, así queda detrás de la nave
            jugador.dibujar_propulsores(PANTALLA)
            jugador.dibujar_escudo(PANTALLA)

            todos_los_sprites.draw(PANTALLA)

            jugador.dibujar_vidas(PANTALLA)

            for enemigo in enemigos: # Dibujamos las vidas de todos los enemigos
                enemigo.dibujar_vidas(PANTALLA)

            jugador.dibujar_disparos_especiales(PANTALLA)
            jugador.dibujar_estado_escudo(PANTALLA)
            jugador.dibujar_estado_dash(PANTALLA)
            jugador.dibujar_experiencia(PANTALLA)

            if esperando_siguiente_ola:
                texto_ola = font_game.render("SIGUIENTE OLEADA...", True, BLANCO)
                PANTALLA.blit(
                    texto_ola,
                    (
                        ANCHO // 2 - texto_ola.get_width() // 2,
                        ALTO // 2 - texto_ola.get_height() // 2
                    )
                )

            
            pygame.display.flip()
            clock.tick(60)

    detener_musica()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
