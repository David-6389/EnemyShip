from enemigos import Enemigo, EnemigoKamikaze, EnemigoTorreta, EnemigoSniper, EnemigoHealer, EnemigoBoss_1


NIVELES = [
    {
        "nombre": "Nivel 1 - Contacto Inicial",
        "olas": [
            {
                # Ola 1: Presentación suave, pocos enemigos, muy débiles.
                "enemigos": [
                    {"tipo": "basico", "cantidad": 3, "vida": 3, "xp": 15, "velocidad": 1.0, "cooldown": 140}
                ]
            },
            {
                # Ola 2: Más enemigos básicos, un poco más rápidos.
                "enemigos": [
                    {"tipo": "basico", "cantidad": 5, "vida": 4, "xp": 15, "velocidad": 1.3, "cooldown": 120}
                ]
            },
            {
                # Ola 3: Introducción del Kamikaze (enseña al jugador a moverse).
                "enemigos": [
                    {"tipo": "basico", "cantidad": 2, "vida": 4, "xp": 15, "velocidad": 1.2},
                    {"tipo": "kamikaze", "cantidad": 2, "vida": 2, "xp": 20, "velocidad": 2.2, "seguimiento": 0.015}
                ]
            }
        ]
    },

    {
        "nombre": "Nivel 2 - Artilleria Pesada",
        "olas": [
            {
                # Ola 1: Introducción de la Torreta (balas radiales).
                "enemigos": [
                    {"tipo": "torreta", "cantidad": 1, "vida": 12, "xp": 40, "velocidad": 1.0, "cooldown": 120, "balas_radiales": 6},
                    {"tipo": "basico", "cantidad": 3, "vida": 5, "xp": 15, "velocidad": 1.4}
                ]
            },
            {
                # Ola 2: Enjambre de Kamikazes.
                "enemigos": [
                    {"tipo": "kamikaze", "cantidad": 5, "vida": 3, "xp": 20, "velocidad": 2.6, "seguimiento": 0.02}
                ]
            },
            {
                # Ola 3: Mezcla de Torretas y Kamikazes (presión a distancia y cuerpo a cuerpo).
                "enemigos": [
                    {"tipo": "torreta", "cantidad": 2, "vida": 12, "xp": 40, "velocidad": 1.0, "cooldown": 110, "balas_radiales": 6},
                    {"tipo": "kamikaze", "cantidad": 3, "vida": 3, "xp": 20, "velocidad": 2.5, "seguimiento": 0.02}
                ]
            }
        ]
    },

    {
        "nombre": "Nivel 3 - Tácticas Enemigas",
        "olas": [
            {
                # Ola 1: Introducción del Healer. El jugador DEBE priorizarlo.
                "enemigos": [
                    {"tipo": "healer", "cantidad": 1, "vida": 10, "xp": 50, "velocidad": 1.5},
                    {"tipo": "torreta", "cantidad": 2, "vida": 14, "xp": 40, "cooldown": 100}
                ]
            },
            {
                # Ola 2: Introducción del Sniper (ataque certero).
                "enemigos": [
                    {"tipo": "sniper", "cantidad": 2, "vida": 6, "xp": 45, "velocidad": 1.0, "cooldown": 200},
                    {"tipo": "kamikaze", "cantidad": 4, "vida": 4, "xp": 22, "velocidad": 2.8, "seguimiento": 0.03}
                ]
            },
            {
                # Ola 3: Sinergia total de mecánicas especiales.
                "enemigos": [
                    {"tipo": "healer", "cantidad": 1, "vida": 12, "xp": 50},
                    {"tipo": "sniper", "cantidad": 1, "vida": 8, "xp": 45, "cooldown": 180},
                    {"tipo": "basico", "cantidad": 4, "vida": 6, "xp": 20, "velocidad": 1.6}
                ]
            }
        ]
    },

    {
        "nombre": "Nivel 4 - El Asedio",
        "olas": [
            {
                # Ola 1: Presión fuerte desde todos los frentes.
                "enemigos": [
                    {"tipo": "torreta", "cantidad": 3, "vida": 15, "xp": 45, "cooldown": 90, "rafaga": 2, "balas_radiales": 8},
                    {"tipo": "kamikaze", "cantidad": 4, "vida": 5, "xp": 25, "velocidad": 3.2, "seguimiento": 0.04}
                ]
            },
            {
                # Ola 2: Enemigos muy resistentes curándose entre sí.
                "enemigos": [
                    {"tipo": "healer", "cantidad": 2, "vida": 12, "xp": 60, "velocidad": 1.6},
                    {"tipo": "basico", "cantidad": 5, "vida": 12, "xp": 25, "velocidad": 1.8, "cooldown": 90, "rafaga": 2}
                ]
            },
            {
                # Ola 3: Caos en pantalla. El jugador necesitará usar Dash y Escudo.
                "enemigos": [
                    {"tipo": "sniper", "cantidad": 2, "vida": 10, "xp": 50, "cooldown": 160},
                    {"tipo": "torreta", "cantidad": 2, "vida": 18, "xp": 50, "cooldown": 80, "rafaga": 3},
                    {"tipo": "kamikaze", "cantidad": 4, "vida": 5, "xp": 25, "velocidad": 3.5, "seguimiento": 0.045}
                ]
            }
        ]
    },

    {
        "nombre": "Nivel 5 - La Guardia Final",
        "olas": [
            {
                # Ola 1: Enjambre brutal de Kamikazes rápidos.
                "enemigos": [
                    {"tipo": "kamikaze", "cantidad": 8, "vida": 6, "xp": 30, "velocidad": 4.0, "seguimiento": 0.06}
                ]
            },
            {
                # Ola 2: La última línea de defensa antes del jefe.
                "enemigos": [
                    {"tipo": "healer", "cantidad": 2, "vida": 15, "xp": 70},
                    {"tipo": "torreta", "cantidad": 3, "vida": 25, "xp": 65, "cooldown": 70, "rafaga": 3, "balas_radiales": 10},
                    {"tipo": "sniper", "cantidad": 2, "vida": 12, "xp": 60, "cooldown": 150}
                ]
            },
            {
                # Ola 3: El JEFE.
                "enemigos": [
                    {"tipo": "jefe", "cantidad": 1, "vida": 150, "xp": 1000}
                ]
            }
        ]
    }
]

def crear_enemigo(tipo_enemigo, jugador_obj, grupo_todos_sprites, grupo_proy_enemigos, recursos_dict, grupo_enemigos):
    if tipo_enemigo == "basico":
        return Enemigo(jugador_obj, grupo_todos_sprites, grupo_proy_enemigos, recursos_dict)

    if tipo_enemigo == "kamikaze":
        return EnemigoKamikaze(jugador_obj, grupo_todos_sprites, grupo_proy_enemigos, recursos_dict)
    
    if tipo_enemigo == "sniper":
        return EnemigoSniper(jugador_obj, grupo_todos_sprites, grupo_proy_enemigos, recursos_dict)

    if tipo_enemigo == "torreta":
        return EnemigoTorreta(jugador_obj, grupo_todos_sprites, grupo_proy_enemigos, recursos_dict)
    
    if tipo_enemigo == "healer":
        return EnemigoHealer(jugador_obj, grupo_todos_sprites, grupo_proy_enemigos, recursos_dict, grupo_enemigos)
    
    if tipo_enemigo == "jefe":
        return EnemigoBoss_1(jugador_obj, grupo_todos_sprites, grupo_proy_enemigos, recursos_dict, grupo_enemigos)

    print(f"Tipo de enemigo desconocido: {tipo_enemigo}")
    return None


def aplicar_configuracion_enemigo(enemigo, config_ola):
    enemigo.vidas = config_ola.get("vida", enemigo.vidas)
    enemigo.vidas_max = enemigo.vidas
    enemigo.xp = config_ola.get("xp", 10)

    if "velocidad" in config_ola:
        enemigo.velocidad = config_ola["velocidad"]

    if "cooldown" in config_ola:
        enemigo.cooldown_base = config_ola["cooldown"]
        enemigo.cooldown = config_ola["cooldown"]

    if "rafaga" in config_ola:
        enemigo.rafaga_total = config_ola["rafaga"]

    if "cooldown_rafaga" in config_ola:
        enemigo.cooldown_rafaga_base = config_ola["cooldown_rafaga"]
        enemigo.cooldown_rafaga = config_ola["cooldown_rafaga"]

    if "balas_radiales" in config_ola:
        enemigo.cantidad_balas = config_ola["balas_radiales"]

    if "seguimiento" in config_ola:
        enemigo.seguimiento = config_ola["seguimiento"]

def generar_ola(nivel, ola, jugador_obj, grupo_enemigos, grupo_todos_sprites, grupo_proy_enemigos, recursos_dict):
    """Genera los enemigos para una ola específica de un nivel."""

    if nivel >= len(NIVELES):
        print("¡Has completado todos los niveles!")
        return False

    if ola >= len(NIVELES[nivel]["olas"]):
        print("La ola indicada no existe.")
        return False

    config_ola = NIVELES[nivel]["olas"][ola]

    print(f"--- Nivel {nivel + 1} - Ola {ola + 1} ---")

    # Compatibilidad:
    # Si la ola tiene "enemigos", mezcla varios tipos.
    # Si no, usa el sistema viejo de un solo tipo.
    configuraciones_enemigos = config_ola.get("enemigos", [config_ola])

    for config_enemigo in configuraciones_enemigos:
        tipo_enemigo = config_enemigo["tipo"]
        cantidad = config_enemigo["cantidad"]

        for _ in range(cantidad):
            nuevo_enemigo = crear_enemigo(
                tipo_enemigo,
                jugador_obj,
                grupo_todos_sprites,
                grupo_proy_enemigos,
                recursos_dict,
                grupo_enemigos
            )

            if nuevo_enemigo is None:
                continue

            aplicar_configuracion_enemigo(nuevo_enemigo, config_enemigo)

            grupo_enemigos.add(nuevo_enemigo)
            grupo_todos_sprites.add(nuevo_enemigo)

    return True