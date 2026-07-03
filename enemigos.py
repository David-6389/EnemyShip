import pygame
import random
import math
import config as cf


class Enemigo(pygame.sprite.Sprite):
    def __init__(self, jugador, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(cf.ROJO)
        self.rect = self.image.get_rect()
        self.jugador = jugador
        self.vidas = 30  #! Vidas ENEMIGO
        self.vidas_max = 30
        self.velocidad = 2
        self.cooldown = 0
        self.proyectiles_disparados = 0
        self.sigue_jugador = False
        self.rect.x = random.randint(0, cf.ANCHO - self.rect.width)
        self.rect.y = random.randint(-self.rect.height, 0)

        self.todos_los_sprites = todos_los_sprites_grupo
        self.proyectiles_enemigos = proyectiles_enemigos_grupo
        self.recursos = recursos_dict

    def update(self):
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia != 0:
            self.rect.x += self.velocidad * dx / distancia
            self.rect.y += self.velocidad * dy / distancia

        # Mantener al enemigo dentro de los límites de la pantalla
        self.rect.x = max(0, min(self.rect.x, cf.ANCHO - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, cf.ALTO - self.rect.height))

        # Disparar al jugador
        if distancia < 200 and self.cooldown == 0:
            if distancia != 0:
                direccion_x = dx / distancia
                direccion_y = dy / distancia
            else:
                direccion_x, direccion_y = 0, 0

            # Decidir si el proyectil sigue al jugador
            if self.proyectiles_disparados % 7 == 0:  # Cada 7 disparos un Disparo especial
                proyectil = ProyectilEnemigo(self.rect.center, dx / distancia, dy / distancia, self.jugador, self.recursos, sigue_jugador=True)
            else:
                proyectil = ProyectilEnemigo(self.rect.center, direccion_x, direccion_y, self.jugador, self.recursos, sigue_jugador=False)

            self.todos_los_sprites.add(proyectil)
            self.proyectiles_enemigos.add(proyectil)
            self.proyectiles_disparados += 1
            self.cooldown = 60  # Configurar el tiempo de enfriamiento

        if self.cooldown > 0:
            self.cooldown -= 1

    def dibujar_vidas(self, pantalla):
        CUBO_VIDA_ENEMY = 10
        espacio_entre_cubos = 0
        x = cf.ANCHO - 10 - ((self.vidas * (CUBO_VIDA_ENEMY + espacio_entre_cubos)))
        y = 10
        for _ in range(self.vidas):
            pygame.draw.rect(pantalla, cf.ROJO, (x, y, CUBO_VIDA_ENEMY, CUBO_VIDA_ENEMY))
            x += CUBO_VIDA_ENEMY + espacio_entre_cubos

    def perder_vida(self, danio=1):
        self.vidas -= danio
        print(self.vidas)
        if self.vidas <= 0:
            self.recursos['sound']['Explocion_Enemigo'].play()
            self.kill()
            return True
        return False


class EnemigoBase(pygame.sprite.Sprite):
    def __init__(self, jugador, vida, velocidad, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Imagen base
        self.rect = self.image.get_rect()

        self.jugador = jugador
        self.vidas = vida
        self.vidas_max = vida
        self.velocidad = velocidad

        # Valor por defecto: subclases que suben hasta una altura fija
        # (EnemigoTorreta, EnemigoHealer, EnemigoBoss_1) lo sobreescriben.
        # Evita AttributeError si alguna subclase futura no lo define
        # y usa el update() heredado de esta clase base.
        self.y_objetivo = 0

        self.rect.x = random.randint(0, cf.ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -50)

        self.todos_los_sprites = todos_los_sprites_grupo
        self.proyectiles_enemigos = proyectiles_enemigos_grupo
        self.recursos = recursos_dict

    def mantener_en_pantalla(self):
        self.rect.x = max(0, min(self.rect.x, cf.ANCHO - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, cf.ALTO - self.rect.height))

    def matar_si_sale_de_pantalla(self, margen=100):
        if (
            self.rect.right < -margen or
            self.rect.left > cf.ANCHO + margen or
            self.rect.bottom < -margen or
            self.rect.top > cf.ALTO + margen
        ):
            self.kill()

    def cambiar_imagen(self, ancho, alto, color):
        centro_anterior = self.rect.center
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = centro_anterior

    def update(self):
        if self.rect.y < self.y_objetivo:
            self.rect.y += self.velocidad
        else:
            self.rect.y = self.y_objetivo
            self.atacar()

    def dibujar_vidas(self, pantalla):
        CUBO_VIDA_ENEMY = 10
        espacio_entre_cubos = 0
        x = cf.ANCHO - 10 - ((self.vidas * (CUBO_VIDA_ENEMY + espacio_entre_cubos)))
        y = 10
        for _ in range(self.vidas):
            pygame.draw.rect(pantalla, cf.ROJO, (x, y, CUBO_VIDA_ENEMY, CUBO_VIDA_ENEMY))
            x += CUBO_VIDA_ENEMY + espacio_entre_cubos

    def perder_vida(self, danio=1):
        self.vidas -= danio
        if self.vidas <= 0:
            self.kill()
            return True  # Murió
        return False  # Sigue vivo


# Enemigo que se lanza a embestir
class EnemigoKamikaze(EnemigoBase):
    def __init__(self, jugador, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict):
        super().__init__(jugador, 3, 2.5, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict)

        self.cambiar_imagen(30, 30, (255, 100, 0))

        self.pos = pygame.math.Vector2(self.rect.center)

        # Arranca bajando
        self.direccion = pygame.math.Vector2(0, 1)
        self.seguimiento = 0.02

        self.danio_contacto = 1
        self.morir_al_chocar = True

    def update(self):
        posicion_jugador = pygame.math.Vector2(self.jugador.rect.center)
        direccion_objetivo = posicion_jugador - self.pos

        if direccion_objetivo.length() > 0:
            direccion_objetivo = direccion_objetivo.normalize()

            # Sigue al jugador de a poco, no instantáneo
            self.direccion = self.direccion.lerp(direccion_objetivo, self.seguimiento)

            if self.direccion.length() > 0:
                self.direccion = self.direccion.normalize()

        self.pos += self.direccion * self.velocidad
        self.rect.center = self.pos

        if not pygame.Rect(-150, -150, cf.ANCHO + 300, cf.ALTO + 300).colliderect(self.rect):
            self.kill()


# Enemigo que dispara ráfagas desde lejos
class EnemigoTorreta(EnemigoBase):
    def __init__(self, jugador, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict):
        super().__init__(jugador, 20, 1, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict)

        self.cambiar_imagen(60, 60, (200, 0, 200))

        self.cooldown_base = 120
        self.cooldown = self.cooldown_base

        self.rafaga_total = 1
        self.rafaga_restante = 0

        self.cooldown_rafaga_base = 25
        self.cooldown_rafaga = self.cooldown_rafaga_base

        self.cantidad_balas = 6
        self.angulo_disparo = 0
        self.cantidad_disparos = 0

        self.y_objetivo = random.randint(60, 180)

    def update(self):
        if self.rect.y < self.y_objetivo:
            self.rect.y += self.velocidad
        else:
            self.rect.y = self.y_objetivo
            self.atacar()

    def atacar(self):
        if self.rafaga_restante > 0 and self.cooldown_rafaga == 0:
            self.disparar()
            self.rafaga_restante -= 1
            self.cooldown_rafaga = self.cooldown_rafaga_base

        elif self.cooldown == 0:
            self.rafaga_restante = self.rafaga_total
            self.cooldown = self.cooldown_base

        if self.cooldown > 0:
            self.cooldown -= 1

        if self.cooldown_rafaga > 0:
            self.cooldown_rafaga -= 1

    def disparar(self):
        self.cantidad_disparos += 1

        if self.cantidad_disparos % 3 == 0:
            self.disparar_al_jugador()
        else:
            self.disparar_radial()

    def disparar_radial(self):
        cantidad_balas = self.cantidad_balas

        for i in range(cantidad_balas):
            angulo = (2 * math.pi / cantidad_balas) * i + self.angulo_disparo

            direccion_x = math.cos(angulo)
            direccion_y = math.sin(angulo)

            proyectil = ProyectilEnemigo(
                self.rect.center,
                direccion_x,
                direccion_y,
                self.jugador,
                self.recursos,
                sigue_jugador=False
            )

            self.todos_los_sprites.add(proyectil)
            self.proyectiles_enemigos.add(proyectil)

        self.angulo_disparo += 0.25

    def disparar_al_jugador(self):
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery
        distancia = max(1, math.sqrt(dx ** 2 + dy ** 2))

        direccion_x = dx / distancia
        direccion_y = dy / distancia

        proyectil = ProyectilEnemigo(
            self.rect.center,
            direccion_x,
            direccion_y,
            self.jugador,
            self.recursos,
            sigue_jugador=False
        )

        self.todos_los_sprites.add(proyectil)
        self.proyectiles_enemigos.add(proyectil)


# Enemigo que dispara rapido y certero desde lejos
class EnemigoSniper(EnemigoBase):
    def __init__(self, jugador, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict):
        super().__init__(jugador, 20, 1, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict)

        self.cambiar_imagen(20, 25, (100, 0, 200))

        self.cooldown_disparo = 300
        self.cooldown = self.cooldown_disparo
        self.velocidad_disparo = 15

        lado = random.choice(["izquierda", "derecha", "arriba", "abajo"])
        margen = 40
        if lado == "izquierda":
            self.rect.left = -10
            self.rect.y = random.randint(50, cf.ALTO - 50)

        elif lado == "derecha":
            self.rect.right = cf.ANCHO + 10
            self.rect.y = random.randint(50, cf.ALTO - 50)

        elif lado == "arriba":
            self.rect.x = random.randint(50, cf.ANCHO - 50)
            self.rect.top = -10

        else:
            self.rect.x = random.randint(50, cf.ANCHO - 50)
            self.rect.bottom = cf.ALTO + 10
        self.objetivo = self.rect.copy()

        if lado == "izquierda":
            self.objetivo.x = margen

        elif lado == "derecha":
            self.objetivo.x = cf.ANCHO - margen - self.rect.width

        elif lado == "arriba":
            self.objetivo.y = margen

        else:
            self.objetivo.y = cf.ALTO - margen - self.rect.height

    def update(self):
        if self.rect.center != self.objetivo.center:
            dx = self.objetivo.centerx - self.rect.centerx
            dy = self.objetivo.centery - self.rect.centery

            distancia = math.hypot(dx, dy)

            if distancia > self.velocidad:
                self.rect.x += int(self.velocidad * dx / distancia)
                self.rect.y += int(self.velocidad * dy / distancia)
            else:
                self.rect.center = self.objetivo.center
        else:
            self.atacar()

    def atacar(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        self.disparo_sniper()

        self.cooldown = self.cooldown_disparo

    def disparo_sniper(self):
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery

        distancia = max(1, math.sqrt(dx ** 2 + dy ** 2))

        direccion_x = dx / distancia
        direccion_y = dy / distancia

        proyectil = ProyectilEnemigo(
            self.rect.center,
            direccion_x,
            direccion_y,
            self.jugador,
            self.recursos,
            sigue_jugador=False,
            velocidad=self.velocidad_disparo  # bala del sniper
        )

        self.todos_los_sprites.add(proyectil)
        self.proyectiles_enemigos.add(proyectil)


# Enemigo que cura a sus aliados, evita al jugador
class EnemigoHealer(EnemigoBase):
    def __init__(self, jugador, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict, grupo_enemigos):
        super().__init__(jugador, 8, 1.5, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict)

        self.cambiar_imagen(35, 35, (0, 255, 150))  # verde curación

        self.grupo_enemigos = grupo_enemigos

        self.cooldown_curacion_base = 100
        self.cooldown_curacion = self.cooldown_curacion_base
        self.radio_curacion = 250
        self.cantidad_curacion = 3
        self.distancia_huida = 300

        self.y_objetivo = random.randint(100, 220)
        self.en_posicion = False

    def update(self):
        # Fase 1: bajar hasta la posición de trabajo
        if not self.en_posicion:
            self.rect.y += self.velocidad
            if self.rect.y >= self.y_objetivo:
                self.rect.y = self.y_objetivo
                self.en_posicion = True
            self.mantener_en_pantalla()
            return  # no cura ni huye hasta estar en posición

        # Fase 2: comportamiento normal (huir / curar)
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery
        distancia = max(1, math.hypot(dx, dy))

        if distancia < self.distancia_huida:
            self.rect.x -= self.velocidad * dx / distancia
            self.rect.y -= self.velocidad * dy / distancia

        self.mantener_en_pantalla()

        if self.cooldown_curacion == 0:
            self.curar_aliado_cercano()
            self.cooldown_curacion = self.cooldown_curacion_base
        else:
            self.cooldown_curacion -= 1

    def curar_aliado_cercano(self):
        mejor_candidato = None
        mayor_deficit = 0

        for enemigo in self.grupo_enemigos:
            if enemigo is self or not hasattr(enemigo, "vidas") or not hasattr(enemigo, "vidas_max"):
                continue

            if enemigo.vidas >= enemigo.vidas_max:
                continue  # ya está a full vida, no hace falta curarlo

            dx = enemigo.rect.centerx - self.rect.centerx
            dy = enemigo.rect.centery - self.rect.centery
            distancia = math.hypot(dx, dy)

            if distancia > self.radio_curacion:
                continue

            deficit = enemigo.vidas_max - enemigo.vidas
            if deficit > mayor_deficit:
                mayor_deficit = deficit
                mejor_candidato = enemigo

        if mejor_candidato:
            mejor_candidato.vidas = min(
                mejor_candidato.vidas_max,
                mejor_candidato.vidas + self.cantidad_curacion
            )
            print(f"Healer curó a un enemigo. Vidas: {mejor_candidato.vidas}/{mejor_candidato.vidas_max}")


class ProyectilEnemigo(pygame.sprite.Sprite):
    def __init__(self, posicion, direccion_x, direccion_y, jugador_obj, recursos_dict, sigue_jugador=False, velocidad=4):
        super().__init__()
        if sigue_jugador:
            self.image = pygame.Surface((9, 9))
            self.image.fill(cf.VERDE)
            self.velocidad = velocidad - 2  # Velocidad más lenta
        else:
            self.image = pygame.Surface((5, 5))
            self.image.fill(cf.ROJO)
            self.velocidad = velocidad  # Velocidad normal
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        self.direccion_x = direccion_x
        self.direccion_y = direccion_y
        self.sigue_jugador = sigue_jugador
        self.jugador = jugador_obj
        self.recursos = recursos_dict
        self.sound_played_esp = False
        self.sound_played = False

    def update(self):
        if self.sigue_jugador:
            # Si el proyectil sigue al jugador, actualizar su dirección
            dx = self.jugador.rect.centerx - self.rect.centerx
            dy = self.jugador.rect.centery - self.rect.centery
            distancia = math.sqrt(dx ** 2 + dy ** 2)
            if not self.sound_played_esp:
                self.recursos['sound']['Proyectil_especial_Enemy'].play()
                self.sound_played_esp = True
                self.sound_played = False
            if distancia != 0:
                self.direccion_x = dx / distancia
                self.direccion_y = dy / distancia
        else:
            if not self.sound_played and not self.sound_played_esp:
                self.recursos['sound']['sound_disp_Enemigo'].play()
                self.sound_played = True

        self.rect.x += self.velocidad * self.direccion_x
        self.rect.y += self.velocidad * self.direccion_y

        if not pygame.Rect(0, 0, cf.ANCHO, cf.ALTO).colliderect(self.rect):
            self.kill()


class EnemigoBoss_1(EnemigoBase):
    def __init__(self, jugador, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict, grupo_enemigos):
        super().__init__(jugador, 150, 1.5, todos_los_sprites_grupo, proyectiles_enemigos_grupo, recursos_dict)

        self.cambiar_imagen(100, 100, (255, 215, 0))  # dorado
        self.rect.centerx = cf.ANCHO // 2
        self.rect.y = -120

        self.grupo_enemigos = grupo_enemigos
        self.danio_contacto = 1  # también hace daño si lo tocás

        self.y_objetivo = 100
        self.en_posicion = False

        self.direccion_patrulla = 1
        self.velocidad_patrulla = 2

        self.fase = 1
        self.invulnerable = False
        self.tiempo_invulnerable = 0

        self.cooldown_ataque_base = 100
        self.cooldown_ataque = self.cooldown_ataque_base
        self.angulo_disparo = 0

        # Dash (fase 2+)
        self.en_dash = False
        self.direccion_dash = pygame.math.Vector2(0, 0)
        self.velocidad_dash = 8
        self.dash_frames = 0
        self.cooldown_dash_base = 220
        self.cooldown_dash = self.cooldown_dash_base

        # Invocación (fase 3)
        self.cooldown_invocar_base = 400
        self.cooldown_invocar = self.cooldown_invocar_base
        self.max_minions = 3

    def update(self):
        # Entrada a pantalla
        if not self.en_posicion:
            self.rect.y += self.velocidad
            if self.rect.y >= self.y_objetivo:
                self.rect.y = self.y_objetivo
                self.en_posicion = True
            return

        self.actualizar_fase()

        if self.invulnerable:
            self.tiempo_invulnerable -= 1
            if self.tiempo_invulnerable <= 0:
                self.invulnerable = False

        if self.en_dash:
            self.mover_dash()
        else:
            self.patrullar()
            self.atacar()

    def actualizar_fase(self):
        ratio = self.vidas / self.vidas_max
        nueva_fase = 1
        if ratio <= 0.4:
            nueva_fase = 3
        elif ratio <= 0.7:
            nueva_fase = 2

        if nueva_fase != self.fase:
            self.fase = nueva_fase
            self.invulnerable = True
            self.tiempo_invulnerable = 60
            print(f"¡El jefe entra en fase {self.fase}!")

    def patrullar(self):
        self.rect.x += self.velocidad_patrulla * self.direccion_patrulla
        if self.rect.left <= 20 or self.rect.right >= cf.ANCHO - 20:
            self.direccion_patrulla *= -1

    def atacar(self):
        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1
        else:
            self.disparo_radial()
            self.cooldown_ataque = self.cooldown_ataque_base

        if self.fase >= 2:
            if self.cooldown_dash > 0:
                self.cooldown_dash -= 1
            else:
                self.iniciar_dash()

        if self.fase >= 3:
            if self.cooldown_invocar > 0:
                self.cooldown_invocar -= 1
            else:
                self.invocar_minion()
                self.cooldown_invocar = self.cooldown_invocar_base

    def disparo_radial(self):
        cantidad = 8 if self.fase == 1 else 12
        for i in range(cantidad):
            angulo = (2 * math.pi / cantidad) * i + self.angulo_disparo
            dx = math.cos(angulo)
            dy = math.sin(angulo)

            proyectil = ProyectilEnemigo(
                self.rect.center, dx, dy, self.jugador, self.recursos, sigue_jugador=False
            )
            self.todos_los_sprites.add(proyectil)
            self.proyectiles_enemigos.add(proyectil)

        self.angulo_disparo += 0.3

    def iniciar_dash(self):
        dx = self.jugador.rect.centerx - self.rect.centerx
        dy = self.jugador.rect.centery - self.rect.centery
        distancia = max(1, math.hypot(dx, dy))

        self.direccion_dash = pygame.math.Vector2(dx / distancia, dy / distancia)
        self.en_dash = True
        self.dash_frames = 40

    def mover_dash(self):
        self.rect.x += self.direccion_dash.x * self.velocidad_dash
        self.rect.y += self.direccion_dash.y * self.velocidad_dash
        self.mantener_en_pantalla()

        self.dash_frames -= 1
        if self.dash_frames <= 0:
            self.en_dash = False
            self.cooldown_dash = self.cooldown_dash_base

    def invocar_minion(self):
        vivos = sum(1 for e in self.grupo_enemigos if e is not self)
        if vivos >= self.max_minions:
            return

        minion = EnemigoKamikaze(self.jugador, self.todos_los_sprites, self.proyectiles_enemigos, self.recursos)
        minion.rect.center = self.rect.center
        self.grupo_enemigos.add(minion)
        self.todos_los_sprites.add(minion)
        print("¡El jefe invocó un minion!")

    def perder_vida(self, danio=1):
        if self.invulnerable:
            return False
        return super().perder_vida(danio)

    def dibujar_vidas(self, pantalla):
        ancho_barra = 400
        alto_barra = 20
        x = cf.ANCHO // 2 - ancho_barra // 2
        y = 20
        ratio = max(0, self.vidas / self.vidas_max)

        pygame.draw.rect(pantalla, (80, 0, 0), (x, y, ancho_barra, alto_barra))
        pygame.draw.rect(pantalla, (255, 215, 0), (x, y, int(ancho_barra * ratio), alto_barra))
        pygame.draw.rect(pantalla, (255, 255, 255), (x, y, ancho_barra, alto_barra), 2)