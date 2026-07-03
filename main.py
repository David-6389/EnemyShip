import sys
import random
import pygame
import menu
import ui  # <- Agregamos ui para el Game Over
import config as cf
import recursos as rec
from jugador import Jugador
import status_game as sg
from potenciadores import Potenciador, PotenciadorVida
from niveles import NIVELES, generar_ola

pygame.init()
recursos = rec.cargar_recursos()

# Inicializar el estado global
sg.estado_juego = sg.EstadoJuego()

# Instanciar jugador y agregarlo al estado global
jugador = Jugador(sg.estado_juego.todos_los_sprites)
sg.estado_juego.jugador = jugador
sg.estado_juego.todos_los_sprites.add(jugador)

pygame.font.init()
FLASH_DURACION = 1

def colision_hitbox_jugador(jugador_sprite, otro_sprite):
    return jugador_sprite.hitbox.colliderect(otro_sprite.rect)

def main():
    clock = pygame.time.Clock()
    mostrando_controles = False
    track_menu_play = False
    jugando = True
    en_menu = True
    opcion_seleccionada = 1
    fondo_y = 0
    flash_tiempo = 0
    flash_color = cf.BLANCO
    
    nivel_actual = 0
    ola_actual = 0
    esperando_siguiente_ola = False
    tiempo_inicio_espera_ola = 0
    DELAY_ENTRE_OLAS = 5000

    # Obtener el fondo desde los recursos de forma segura
    fondo = recursos['imagenes']['fondo']
    fondo_rect = fondo.get_rect()

    while jugando:
        rec.reproducir_musica('soundtrack_menu', 0.6)
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
                            rec.reproducir_musica('soundtrack_juego', 0.6)
                            track_menu_play = False

                            # Usamos el método limpio del estado global
                            sg.estado_juego.reiniciar(cf)

                            nivel_actual = 0
                            ola_actual = 0
                            generar_ola(
                                nivel_actual,
                                ola_actual,
                                sg.estado_juego.jugador,
                                sg.estado_juego.enemigos,
                                sg.estado_juego.todos_los_sprites,
                                sg.estado_juego.proyectiles_enemigos,
                                recursos
                            )
                        elif opcion_seleccionada == 2:  # Controles
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
                        menu.mostrar_menu_mejoras(cf.PANTALLA, sg.estado_juego.jugador)
                    elif evento.key == pygame.K_c:
                        sg.estado_juego.jugador.activar_escudo()
                    elif evento.key == pygame.K_LSHIFT:
                        sg.estado_juego.jugador.activar_dash()
                    elif evento.key == pygame.K_SPACE and not bullet_fired:
                        sg.estado_juego.jugador.disparar(sg.estado_juego.bullet, sg.estado_juego.todos_los_sprites)
                        bullet_fired = True
                    elif evento.key == pygame.K_LCTRL:
                        if sg.estado_juego.enemigos:
                            enemigo_objetivo = sg.estado_juego.enemigos.sprites()[0]
                            sg.estado_juego.jugador.disparar_especial(sg.estado_juego.bullet_especial, sg.estado_juego.todos_los_sprites, enemigo_objetivo)
                    elif evento.key == pygame.K_ESCAPE:
                        en_menu = True
                        mostrando_controles = False
                        if not track_menu_play:
                            rec.detener_musica()
                            rec.reproducir_musica('soundtrack_menu', 0.6)
                            track_menu_play = True
        
        # Renderizado y lógicas
        if en_menu:
            menu.mostrar_menu(cf.PANTALLA, opcion_seleccionada)
        elif mostrando_controles:
            menu.mostrar_controles(cf.PANTALLA)
        else:
            sg.estado_juego.todos_los_sprites.update()

            # Mover el fondo hacia arriba
            fondo_y -= 1
            if fondo_y <= - fondo_rect.height:
                fondo_y = 0

            # Colisión: proyectiles enemigos contra jugador
            if pygame.sprite.spritecollide(sg.estado_juego.jugador, sg.estado_juego.proyectiles_enemigos, True, colision_hitbox_jugador):
                flash_tiempo = FLASH_DURACION
                flash_color = cf.BLANCO
                recursos['sound']['colision'].play()

                jugador_muerto = sg.estado_juego.jugador.perder_vida(cf.DANIO_DISPARO_NORMAL)

                if jugador_muerto:
                    ui.mostrar_mensaje_Game_over()
                    rec.detener_musica()
                    rec.reproducir_musica('soundtrack_menu', 0.6)
                    en_menu = True
                    mostrando_controles = False
                    esperando_siguiente_ola = False
                    tiempo_inicio_espera_ola = 0

            # Colisión: enemigos contra jugador
            colision_enemigo_jugador = pygame.sprite.spritecollide(sg.estado_juego.jugador, sg.estado_juego.enemigos, False, colision_hitbox_jugador)
            jugador_muerto_por_contacto = False
            
            for enemigo_contacto in colision_enemigo_jugador:
                danio = getattr(enemigo_contacto, "danio_contacto", 0)
                if danio > 0:
                    flash_tiempo = FLASH_DURACION
                    flash_color = cf.ROJO
                    recursos['sound']['colision'].play()

                    for _ in range(danio):
                        jugador_muerto_por_contacto = sg.estado_juego.jugador.perder_vida(cf.DANIO_DISPARO_NORMAL)

                    if getattr(enemigo_contacto, "morir_al_chocar", False):
                        enemigo_contacto.kill()

                    if jugador_muerto_por_contacto:
                        break

            if jugador_muerto_por_contacto:
                ui.mostrar_mensaje_Game_over()
                rec.detener_musica()
                rec.reproducir_musica('soundtrack_menu', 0.6)
                en_menu = True
                mostrando_controles = False
                esperando_siguiente_ola = False
                tiempo_inicio_espera_ola = 0

            # Colisión: balas normales contra enemigos
            impactos_enemigos = pygame.sprite.groupcollide(sg.estado_juego.bullet, sg.estado_juego.enemigos, False, False)

            for proyectil, enemigos_afectados in impactos_enemigos.items():
                for enemigo_afectado in enemigos_afectados:
                    murio_enemigo = enemigo_afectado.perder_vida(cf.DANIO_DISPARO_NORMAL)
                    recursos['sound']['colision'].play()
                    proyectil.kill()
                    proyectil.colisionar_enemigo(sg.estado_juego.grupo_potenciadores, sg.estado_juego.todos_los_sprites)

                    if murio_enemigo:
                        xp_ganada = getattr(enemigo_afectado, "xp", 10)
                        sg.estado_juego.jugador.ganar_experiencia(xp_ganada)

            # Colisión: disparos especiales contra enemigos
            impactos_especiales_enemigos = pygame.sprite.groupcollide(sg.estado_juego.bullet_especial, sg.estado_juego.enemigos, True, False)

            for proyectil_especial, enemigos_afectados in impactos_especiales_enemigos.items():
                for enemigo_afectado in enemigos_afectados:
                    murio_enemigo = enemigo_afectado.perder_vida(cf.DANIO_DISPARO_ESPECIAL)
                    recursos['sound']['colision'].play()

                    if murio_enemigo:
                        xp_ganada = getattr(enemigo_afectado, "xp", 10)
                        sg.estado_juego.jugador.ganar_experiencia(xp_ganada)

            # Control de fin de oleada
            if not sg.estado_juego.enemigos and not en_menu and not esperando_siguiente_ola:
                esperando_siguiente_ola = True
                tiempo_inicio_espera_ola = pygame.time.get_ticks()

                chance = random.random()
                if chance < 0.99: 
                    potenciador_vida = PotenciadorVida()
                    sg.estado_juego.todos_los_sprites.add(potenciador_vida)
                    sg.estado_juego.grupo_potenciadores_vida.add(potenciador_vida)
                elif sg.estado_juego.jugador.puntos_habilidad > 0:
                    menu.mostrar_menu_mejoras(cf.PANTALLA, sg.estado_juego.jugador)                  

            # Siguiente oleada
            if esperando_siguiente_ola:
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - tiempo_inicio_espera_ola >= DELAY_ENTRE_OLAS:
                    esperando_siguiente_ola = False
                    ola_actual += 1

                    if ola_actual >= len(NIVELES[nivel_actual]["olas"]):
                        nivel_actual += 1
                        ola_actual = 0

                    if not generar_ola(nivel_actual, ola_actual, sg.estado_juego.jugador, sg.estado_juego.enemigos, sg.estado_juego.todos_los_sprites, sg.estado_juego.proyectiles_enemigos, recursos):
                        ui.mostrar_mensaje_WIN()  # Llamamos al final del juego si ganas todo!
                        en_menu = True

            # Limpiar colisiones de proyectiles contra proyectiles
            pygame.sprite.groupcollide(sg.estado_juego.bullet, sg.estado_juego.proyectiles_enemigos, True, True)
            pygame.sprite.groupcollide(sg.estado_juego.bullet_especial, sg.estado_juego.proyectiles_enemigos, True, True)

            # Agarrar Scrap
            colision_scrap = pygame.sprite.spritecollide(sg.estado_juego.jugador, sg.estado_juego.grupo_scrap_perdido, True)
            for scrap_recuperado in colision_scrap:
                sg.estado_juego.jugador.scrap += scrap_recuperado.cantidad
                recursos['sound']['sound_Potenciador'].play()       

            # Agarrar potenciador disparos especiales
            colisiones_potenciador = pygame.sprite.spritecollide(sg.estado_juego.jugador, sg.estado_juego.grupo_potenciadores, True)
            for _ in colisiones_potenciador:
                recursos['sound']['sound_Potenciador'].play()
                sg.estado_juego.jugador.disparos_especial += 3

            # Agarrar potenciador vida
            colisiones_vida = pygame.sprite.spritecollide(sg.estado_juego.jugador, sg.estado_juego.grupo_potenciadores_vida, True)
            for _ in colisiones_vida:
                sg.estado_juego.jugador.vidas += 1
                recursos['sound']['sound_Potenciador'].play()
                
            # Dibujado de pantalla
            if flash_tiempo > 0:
                cf.PANTALLA.fill(flash_color)
                flash_tiempo -= 1
            else:
                cf.PANTALLA.blit(fondo, (0, fondo_y))
                cf.PANTALLA.blit(fondo, (0, fondo_y + fondo_rect.height))
                cf.PANTALLA.fill(cf.NEGRO, special_flags=pygame.BLEND_RGB_ADD)

            # Dibujar elementos del jugador
            sg.estado_juego.jugador.dibujar_propulsores(cf.PANTALLA)
            sg.estado_juego.jugador.dibujar_escudo(cf.PANTALLA)
            sg.estado_juego.todos_los_sprites.draw(cf.PANTALLA)
            sg.estado_juego.jugador.dibujar_vidas(cf.PANTALLA)

            # Dibujar vidas enemigas
            for enemigo in sg.estado_juego.enemigos: 
                enemigo.dibujar_vidas(cf.PANTALLA)

            # UI HUD
            sg.estado_juego.jugador.dibujar_disparos_especiales(cf.PANTALLA)
            sg.estado_juego.jugador.dibujar_estado_escudo(cf.PANTALLA)
            sg.estado_juego.jugador.dibujar_estado_dash(cf.PANTALLA)
            sg.estado_juego.jugador.dibujar_experiencia(cf.PANTALLA)

            if esperando_siguiente_ola:
                texto_ola = recursos['font']['font_game'].render("SIGUIENTE OLEADA...", True, cf.BLANCO)
                cf.PANTALLA.blit(texto_ola, (cf.ANCHO // 2 - texto_ola.get_width() // 2, cf.ALTO // 2 - texto_ola.get_height() // 2))

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()