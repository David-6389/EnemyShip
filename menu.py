import sys
import os
import pygame
import config as cf
import recursos as rec

pygame.init()

SELECCION = (169, 50, 38)
TECLAS = (17, 120, 100)

# ============================================================
# MENU PRINCIPAL
# ============================================================
def mostrar_menu(pantalla, opcion_seleccionada):
    recursos = rec.cargar_recursos()
    
    # Cargamos y escalamos el fondo desde el caché
    fondo_menu = recursos['imagenes']['fondo_menu']
    fondo_menu = pygame.transform.scale(fondo_menu, (cf.ANCHO, cf.ALTO))
    pantalla.blit(fondo_menu, (0, 0))
    
    # 1. Definimos la ruta de la fuente manualmente
    directorio_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(directorio_base, 'font', 'font_menu.TTF')
    
    # 2. Instanciamos con los tamaños correctos
    fuente_menu_select = pygame.font.Font(font_path, 50) 
    fuente_menu = pygame.font.Font(font_path, 40)

    opciones = ["JUGAR", "CONTROLES", "SALIR"]
    menu_y = cf.ALTO // 2 - (len(opciones) * 50) // 2

    for i, opcion in enumerate(opciones):
        if i == opcion_seleccionada - 1:
            texto = fuente_menu_select.render(opcion, True, SELECCION)
        else:
            texto = fuente_menu.render(opcion, True, cf.BLANCO)
            
        texto_x = cf.ANCHO // 2 - texto.get_width() // 2
        texto_y = menu_y + i * 100
        pantalla.blit(texto, (texto_x, texto_y))
    
    pygame.display.flip()

# ============================================================
# MENU DE MEJORAS / INVENTARIO
# ============================================================
def mostrar_menu_mejoras(pantalla, jugador):
    recursos = rec.cargar_recursos()
    
    fondo_menu = recursos['imagenes']['fondo_menu']
    fondo_menu = pygame.transform.scale(fondo_menu, (cf.ANCHO, cf.ALTO))
    
    # 1. Definimos la ruta de la fuente
    directorio_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(directorio_base, 'font', 'font_menu.TTF')
    
    # 2. Asignamos a las fuentes correspondientes
    fuente_titulo = pygame.font.Font(font_path, 45)
    fuente_opcion = pygame.font.Font(font_path, 30)
    fuente_opcion_sel = pygame.font.Font(font_path, 35)
    fuente_info = pygame.font.Font(font_path, 28)

    opcion_seleccionada = 0

    opciones = [
        {"texto": "Mejorar Vida Maxima (+1) - Costo: 1 punto", "atributo": "vidas", "costo": 1, "mejora": 1},
        {"texto": "Mejorar Velocidad (+0.3) - Costo: 1 punto", "atributo": "speed_up", "costo": 1, "mejora": 0.3},
        {"texto": "Mejorar Velocidad Reversa (+0.3) - Costo: 1 punto", "atributo": "speed_down", "costo": 1, "mejora": 0.3},
        {"texto": "Mejorar Giro (+0.3) - Costo: 1 punto", "atributo": "speed_sides", "costo": 1, "mejora": 0.3},
        {"texto": "Sumar Disparo Especial (+1) - Costo: 1 punto", "atributo": "disparos_especial", "costo": 1, "mejora": 1},
        {"texto": "Escudo", "atributo": "escudo", "especial": "escudo"},
        {"texto": "Dash", "atributo": "dash", "especial": "dash"},
        {"texto": "Salir", "accion": "salir"}
    ]

    en_menu_mejoras = True

    while en_menu_mejoras:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rec.detener_musica()
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    opcion = opciones[opcion_seleccionada]

                    if opcion.get("accion") == "salir":
                        en_menu_mejoras = False

                    elif opcion.get("especial") == "escudo":
                        if jugador.escudo_nivel >= jugador.escudo_nivel_max:
                            print("Escudo al nivel máximo.")
                        else:
                            costo = 2 if jugador.escudo_nivel == 0 else 1
                            if jugador.puntos_habilidad >= costo:
                                jugador.puntos_habilidad -= costo
                                jugador.escudo_nivel += 1
                                print(f"Escudo nivel {jugador.escudo_nivel} desbloqueado/mejorado")
                            else:
                                print("No tenés puntos de habilidad suficientes.")

                    elif opcion.get("especial") == "dash":
                        if jugador.dash_nivel >= jugador.dash_nivel_max:
                            print("Dash al nivel máximo.")
                        else:
                            costo = 2 if jugador.dash_nivel == 0 else 1
                            if jugador.puntos_habilidad >= costo:
                                jugador.puntos_habilidad -= costo
                                jugador.dash_nivel += 1
                                print(f"Dash nivel {jugador.dash_nivel} desbloqueado/mejorado")
                            else:
                                print("No tenés puntos de habilidad suficientes.")

                    elif jugador.puntos_habilidad >= opcion["costo"]:
                        jugador.puntos_habilidad -= opcion["costo"]
                        valor_actual = getattr(jugador, opcion["atributo"])
                        setattr(jugador, opcion["atributo"], valor_actual + opcion["mejora"])
                        print(f"Mejora comprada: {opcion['texto']}")
                        print(f"Puntos restantes: {jugador.puntos_habilidad}")
                    else:
                        print("No tenés puntos de habilidad suficientes.")

                elif evento.key == pygame.K_ESCAPE:
                    en_menu_mejoras = False

        pantalla.blit(fondo_menu, (0, 0))

        texto_titulo = fuente_titulo.render("INVENTARIO / HABILIDADES", True, cf.BLANCO)
        pantalla.blit(texto_titulo, (cf.ANCHO // 2 - texto_titulo.get_width() // 2, 80))

        texto_puntos = fuente_info.render(f"Puntos disponibles: {jugador.puntos_habilidad}", True, (255, 255, 0))
        pantalla.blit(texto_puntos, (cf.ANCHO // 2 - texto_puntos.get_width() // 2, 150))

        texto_stats = fuente_info.render(
            f"Vida: {jugador.vidas} | Velocidad: {round(jugador.speed_up, 1)} | Giro: {round(jugador.speed_sides, 1)} | Especiales: {jugador.disparos_especial}",
            True, cf.BLANCO
        )
        pantalla.blit(texto_stats, (cf.ANCHO // 2 - texto_stats.get_width() // 2, 190))

        menu_y = 270

        for i, opcion in enumerate(opciones):
            if opcion.get("especial") == "escudo":
                if jugador.escudo_nivel == 0:
                    texto_opcion = "Desbloquear Escudo - Costo: 2 puntos"
                elif jugador.escudo_nivel < jugador.escudo_nivel_max:
                    texto_opcion = f"Mejorar Escudo (Nivel {jugador.escudo_nivel}→{jugador.escudo_nivel+1}) - Costo: 1 punto"
                else:
                    texto_opcion = "Escudo: NIVEL MÁXIMO"

            elif opcion.get("especial") == "dash":
                if jugador.dash_nivel == 0:
                    texto_opcion = "Desbloquear Dash - Costo: 2 puntos"
                elif jugador.dash_nivel < jugador.dash_nivel_max:
                    texto_opcion = f"Mejorar Dash (Nivel {jugador.dash_nivel}→{jugador.dash_nivel+1}) - Costo: 1 punto"
                else:
                    texto_opcion = "Dash: NIVEL MÁXIMO"
                    
            else:
                texto_opcion = opcion["texto"]
                
            if i == opcion_seleccionada:
                texto = fuente_opcion_sel.render(texto_opcion, True, SELECCION)
            else:
                texto = fuente_opcion.render(texto_opcion, True, cf.BLANCO)

            texto_x = cf.ANCHO // 2 - texto.get_width() // 2
            texto_y = menu_y + i * 65
            pantalla.blit(texto, (texto_x, texto_y))

        pygame.display.flip()

# ============================================================
# CONTROLES
# ============================================================
def mostrar_controles(pantalla):
    recursos = rec.cargar_recursos()
    
    fondo_menu = recursos['imagenes']['fondo_menu']
    fondo_menu = pygame.transform.scale(fondo_menu, (cf.ANCHO, cf.ALTO))
    pantalla.blit(fondo_menu, (0, 0))
    
    # 1. Definimos la ruta y fuente
    directorio_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(directorio_base, 'font', 'font_menu.TTF')
    fuente_menu = pygame.font.Font(font_path, 40)
    
    controles = [
        "Arriba: UP", "Abajo: DOWN", "Izquierda: LEFT", "Derecha: RIGHT", 
        "Disparar: SPACE", "-- ESPECIALES --", "Disparo Especial: CTRL", 
        "Escudo: C", "Dash: SHIFT"
    ]
   
    for i, control in enumerate(controles):
        partes = control.split(":")
        texto_control = partes[0] + (":" if len(partes) > 1 else "")
        texto_tecla = partes[1] if len(partes) > 1 else ""
        
        texto_control_renderizado = fuente_menu.render(texto_control, True, SELECCION)
        texto_tecla_renderizado = fuente_menu.render(texto_tecla, True, TECLAS)

        texto_x_control = cf.ANCHO // 4 - texto_control_renderizado.get_width() // 2  
        texto_y_control = cf.ALTO // 2 - len(controles) * 25 + i * 50  

        texto_x_tecla = cf.ANCHO // 2  
        texto_y_tecla = texto_y_control + (texto_tecla_renderizado.get_height() - texto_control_renderizado.get_height()) // 2
        
        pantalla.blit(texto_control_renderizado, (texto_x_control, texto_y_control))
        if texto_tecla:
            pantalla.blit(texto_tecla_renderizado, (texto_x_tecla, texto_y_tecla))
    
    pygame.display.flip()