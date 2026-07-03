# status_game.py
import pygame

class EstadoJuego:
    def __init__(self):
        # Grupos de sprites centralizados
        self.todos_los_sprites = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.proyectiles_enemigos = pygame.sprite.Group()
        self.bullet = pygame.sprite.Group()
        self.bullet_especial = pygame.sprite.Group()
        self.grupo_potenciadores = pygame.sprite.Group()
        self.lista_sprites_puntos_atributos = pygame.sprite.Group()
        self.grupo_scrap_perdido = pygame.sprite.Group()
        self.grupo_potenciadores_vida = pygame.sprite.Group()

        self.jugador = None

        # Variables de progresión
        self.nivel_actual = 0
        self.ola_actual = 0
        self.esperando_siguiente_ola = False
        self.tiempo_inicio_espera_ola = 0

    def vaciar_grupos(self):
        """Limpia todos los grupos excepto el jugador."""
        self.todos_los_sprites.empty()
        self.enemigos.empty()
        self.proyectiles_enemigos.empty()
        self.bullet.empty()
        self.bullet_especial.empty()
        self.grupo_potenciadores.empty()
        self.lista_sprites_puntos_atributos.empty()
        self.grupo_scrap_perdido.empty()
        self.grupo_potenciadores_vida.empty()

        if self.jugador:
            self.todos_los_sprites.add(self.jugador)

    def reiniciar(self, config):
        if self.jugador:
            self.jugador.rect.center = (config.ANCHO / 2, config.ALTO - 25)
            self.jugador.vidas = config.VIDAS_INICIALES_JUGADOR
            self.jugador.disparos_especial = config.DISPAROS_ESPECIALES_INICIALES
            self.jugador.angle = 0
            self.jugador.scrap = config.SCRAP_INICIAL
            self.jugador.experiencia = 0
            self.jugador.nivel_jugador = 1
        
        self.vaciar_grupos()

# Instancia global para importar desde cualquier archivo
estado_juego = EstadoJuego()