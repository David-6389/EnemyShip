import pygame
import config as cf
import recursos as rec

#? GAME OVER
def mostrar_mensaje_Game_over():
    # Superponer un rectángulo semitransparente sobre toda la pantalla
    overlay = pygame.Surface((cf.ANCHO, cf.ALTO), pygame.SRCALPHA)
    overlay.fill(cf.GAME_OVER)
    cf.PANTALLA.blit(overlay, (0, 0))

    # Obtenemos los recursos de forma segura con el nuevo sistema
    recursos = rec.cargar_recursos()
    texto = recursos['font']['font_game'].render("GAME OVER", True, cf.BLANCO)
    cf.PANTALLA.blit(texto, ((cf.ANCHO - texto.get_width()) // 2, (cf.ALTO - texto.get_height()) // 2))
    
    pygame.display.flip()
    pygame.time.delay(2000)

#? WINNER
def mostrar_mensaje_WIN():
    overlay = pygame.Surface((cf.ANCHO, cf.ALTO), pygame.SRCALPHA)
    overlay.fill(cf.GAME_OVER)
    cf.PANTALLA.blit(overlay, (0, 0))

    # Obtenemos los recursos de forma segura con el nuevo sistema
    recursos = rec.cargar_recursos()
    
    texto_inicial = recursos['font']['font_game'].render("GANASTE !!!", True, cf.BLANCO)
    cf.PANTALLA.blit(texto_inicial, ((cf.ANCHO - texto_inicial.get_width()) // 2, (cf.ALTO - texto_inicial.get_height()) // 2))
    pygame.display.flip()
    pygame.time.delay(1000)

    texto_final = recursos['font']['font_game'].render("CONTINUARA...", True, cf.BLANCO)
    cf.PANTALLA.blit(texto_final, ((cf.ANCHO - texto_final.get_width()) // 2, (cf.ALTO - texto_final.get_height()) // 1.7))
    pygame.display.flip()
    pygame.time.delay(2500)