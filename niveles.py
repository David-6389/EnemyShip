from enemigos import Enemigo, EnemigoKamikaze, EnemigoTorreta, EnemigoSniper, EnemigoHealer, EnemigoBoss_1


NIVELES = [
        {
            "nombre": "Nivel 1 - Patrulla inicial",
            "olas": [
                {
                "enemigos": [
                    {
                        "tipo": "basico",
                        "cantidad": 1,
                        "vida": 1,
                        "xp": 22,
                        "velocidad": 2,
                        "cooldown": 80,
                        "rafaga": 1,
                        "cooldown_rafaga": 15,
                        "balas_radiales": 6
                    },
                    {
                    "tipo": "healer",
                    "cantidad": 1,
                    "vida": 10,
                    "xp": 2000
                    },  
                ]},
                {
                "tipo": "healer",
                "cantidad": 1,
                "vida": 8,
                "xp": 30
                },  
                {
                    "tipo": "sniper",
                    "cantidad": 3,
                    "vida": 2,
                    "xp": 12,
                    "seguimiento": 0.01,
                    "cooldown": 200
                },
                {
                    "tipo": "basico",
                    "cantidad": 3,
                    "vida": 6,
                    "xp": 10,
                    "velocidad": 1.0,
                    "cooldown": 140,
                    "rafaga": 1,
                    "cooldown_rafaga": 25,
                    "balas_radiales": 3
                },
                {
                    "tipo": "kamikaze",
                    "cantidad": 3,
                    "vida": 2,
                    "xp": 12,
                    "velocidad": 2.4,
                    "seguimiento": 0.015
                },
                {
                    "tipo": "sniper",
                    "cantidad": 1,
                    "vida": 2,
                    "xp": 12,
                    "seguimiento": 0.01,
                    "cooldown": 200
                },
                {
                    "tipo": "torreta",
                    "cantidad": 1,
                    "vida": 10,
                    "xp": 25,
                    "velocidad": 0.8,
                    "cooldown": 130,
                    "rafaga": 1,
                    "cooldown_rafaga": 25,
                    "balas_radiales": 5
                },
            ]
        },

        {
            "nombre": "Nivel 2 - Presion enemiga",
            "olas": [
                {
                    "tipo": "basico",
                    "cantidad": 4,
                    "vida": 8,
                    "xp": 12,
                    "velocidad": 1.2,
                    "cooldown": 120,
                    "rafaga": 1,
                    "cooldown_rafaga": 22,
                    "balas_radiales": 4
                },
                {
                    "tipo": "torreta",
                    "cantidad": 2,
                    "vida": 12,
                    "xp": 30,
                    "velocidad": 1.0,
                    "cooldown": 115,
                    "rafaga": 1,
                    "cooldown_rafaga": 22,
                    "balas_radiales": 6
                },
                {
                    "tipo": "kamikaze",
                    "cantidad": 4,
                    "vida": 3,
                    "xp": 16,
                    "velocidad": 2.9,
                    "seguimiento": 0.025
                },
            ]
        },

        {
            "nombre": "Nivel 3 - Zona hostil",
            "olas": [
                {
                    "tipo": "torreta",
                    "cantidad": 2,
                    "vida": 14,
                    "xp": 40,
                    "velocidad": 1.2,
                    "cooldown": 100,
                    "rafaga": 2,
                    "cooldown_rafaga": 20,
                    "balas_radiales": 7
                },
                {
                    "tipo": "kamikaze",
                    "cantidad": 5,
                    "vida": 3,
                    "xp": 20,
                    "velocidad": 3.2,
                    "seguimiento": 0.035
                },
                {
                    "tipo": "basico",
                    "cantidad": 5,
                    "vida": 10,
                    "xp": 18,
                    "velocidad": 1.5,
                    "cooldown": 100,
                    "rafaga": 1,
                    "cooldown_rafaga": 18,
                    "balas_radiales": 5
                },
            ]
        },

        {
        "nombre": "Nivel 4 - Ataque coordinado",
        "olas": [
            {
                "enemigos": [
                    {
                        "tipo": "basico",
                        "cantidad": 4,
                        "vida": 11,
                        "xp": 18,
                        "velocidad": 1.6,
                        "cooldown": 95,
                        "rafaga": 1,
                        "cooldown_rafaga": 18,
                        "balas_radiales": 5
                    },
                    {
                        "tipo": "kamikaze",
                        "cantidad": 3,
                        "vida": 4,
                        "xp": 22,
                        "velocidad": 3.4,
                        "seguimiento": 0.04
                    }
                ]
            },
            {
                "enemigos": [
                    {
                        "tipo": "torreta",
                        "cantidad": 2,
                        "vida": 17,
                        "xp": 45,
                        "velocidad": 1.3,
                        "cooldown": 85,
                        "rafaga": 2,
                        "cooldown_rafaga": 16,
                        "balas_radiales": 8
                    },
                    {
                        "tipo": "kamikaze",
                        "cantidad": 4,
                        "vida": 4,
                        "xp": 22,
                        "velocidad": 3.7,
                        "seguimiento": 0.045
                    }
                ]
            },
            {
                "enemigos": [
                    {
                        "tipo": "basico",
                        "cantidad": 4,
                        "vida": 13,
                        "xp": 20,
                        "velocidad": 1.8,
                        "cooldown": 85,
                        "rafaga": 1,
                        "cooldown_rafaga": 16,
                        "balas_radiales": 6
                    },
                    {
                        "tipo": "torreta",
                        "cantidad": 2,
                        "vida": 19,
                        "xp": 50,
                        "velocidad": 1.5,
                        "cooldown": 75,
                        "rafaga": 3,
                        "cooldown_rafaga": 15,
                        "balas_radiales": 10
                    },
                    {
                        "tipo": "kamikaze",
                        "cantidad": 3,
                        "vida": 4,
                        "xp": 24,
                        "velocidad": 3.8,
                        "seguimiento": 0.05
                    }
                ]
            }
        ]
    },
    {
        "nombre": "Nivel 5 - Ultima defensa",
        "olas": [
            {
                "enemigos": [
                    {
                        "tipo": "basico",
                        "cantidad": 5,
                        "vida": 14,
                        "xp": 22,
                        "velocidad": 1.9,
                        "cooldown": 80,
                        "rafaga": 1,
                        "cooldown_rafaga": 15,
                        "balas_radiales": 6
                    },
                    {
                        "tipo": "torreta",
                        "cantidad": 1,
                        "vida": 20,
                        "xp": 55,
                        "velocidad": 1.5,
                        "cooldown": 70,
                        "rafaga": 2,
                        "cooldown_rafaga": 14,
                        "balas_radiales": 10
                    }
                ]
            },
            {
                "enemigos": [
                    {
                        "tipo": "kamikaze",
                        "cantidad": 7,
                        "vida": 5,
                        "xp": 25,
                        "velocidad": 4.0,
                        "seguimiento": 0.06
                    },
                    {
                        "tipo": "torreta",
                        "cantidad": 2,
                        "vida": 21,
                        "xp": 55,
                        "velocidad": 1.6,
                        "cooldown": 65,
                        "rafaga": 3,
                        "cooldown_rafaga": 13,
                        "balas_radiales": 11
                    }
                ]
            },
            {
                "enemigos": [
                    {
                        "tipo": "basico",
                        "cantidad": 5,
                        "vida": 16,
                        "xp": 25,
                        "velocidad": 2.0,
                        "cooldown": 70,
                        "rafaga": 1,
                        "cooldown_rafaga": 14,
                        "balas_radiales": 7
                    },
                    {
                        "tipo": "kamikaze",
                        "cantidad": 6,
                        "vida": 5,
                        "xp": 28,
                        "velocidad": 4.2,
                        "seguimiento": 0.065
                    },
                    {
                        "tipo": "torreta",
                        "cantidad": 3,
                        "vida": 24,
                        "xp": 60,
                        "velocidad": 1.8,
                        "cooldown": 55,
                        "rafaga": 3,
                        "cooldown_rafaga": 12,
                        "balas_radiales": 12
                    }
                ]
            },
            { # Boss final
                "tipo": "jefe",
                "cantidad": 1,
                "vida": 150,
                "xp": 500
            },
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