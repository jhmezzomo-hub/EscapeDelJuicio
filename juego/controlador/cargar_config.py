import pygame

def get_config_sala(nombre_sala):
    configs = {
        "inicio": {
            "fondo": "Fondo_sala1",
            "nombre_carpeta": "Fondos",
            "personaje": {
                
                "pos_inicial": (100, 400),
                "tamaño": (50, 70),
                "pos_final":(770, 400),
            },
            "puertas": {
                "salida": pygame.Rect(770, 400, 70, 40)
            },
            "sala_anterior": None,
            "siguiente_sala": "sala2"
        },
        "sala2": {
            "fondo": "Fondo_sala1",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (100, 400),
                "tamaño": (50, 70),
            },
            "caption": "Sala 2",
            "puertas": {
                "volver": pygame.Rect(100, 400, 70, 40),
                "salida": pygame.Rect(770, 400, 70, 40)
            },
            
            "sala_anterior": "inicio",
            "siguiente_sala": "sala3"
        }
    }
    return configs.get(nombre_sala, None)