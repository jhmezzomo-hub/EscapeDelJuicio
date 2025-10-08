import pygame
def get_config_sala(nombre_sala, screen):
    configs = {
        "inicio": {
            "fondo": "Fondo_sala1",
            "nombre_carpeta": "Fondos",
            "WIDTH": 1100,
            "HEIGHT": 600,
            "personaje": {
                "pos_inicial": (100, 400),
                "tamaño": (50, 70),
                "velocidad": 5
            },
            "caption": "Escape Del Juicio",
            "screen": screen,
            "puertas": {
                "salida": pygame.Rect(770, 400, 70, 40)
            },
            "siguiente_sala": "sala2"
        },
        "sala2": {
            "fondo": "Fondo_sala1",
            "nombre_carpeta": "Fondos",
            "WIDTH": 1100,
            "HEIGHT": 600,
            "personaje": {
                "pos_inicial": (100, 400),
                "tamaño": (50, 70),
                "velocidad": 5
            },
            "caption": "Sala 2",
            "screen": screen,
            "puertas": {
                "volver": pygame.Rect(100, 400, 70, 40),
                "salida": pygame.Rect(770, 400, 70, 40)
            },
            
            "sala_anterior": "inicio",
            "siguiente_sala": "sala3"
        }
    }
    
    return configs.get(nombre_sala)