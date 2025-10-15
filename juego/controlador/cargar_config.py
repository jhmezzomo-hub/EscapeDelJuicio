import pygame

def get_config_sala(nombre_sala):
    configs = {
        "inicio": {
            "fondo": "Fondo_inicial.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                
                "pos_inicial": (100, 400),
                "tamaño": (125, 150),
                "pos_final":(770, 400),
            },
            "puertas": {
                "salida": pygame.Rect(770, 400, 70, 40)
            },
            "sala_anterior": None,
            "siguiente_sala": "sala2"
        },
        "sala2": {
            "fondo": "Fondo_sala1.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (100, 400),
                "tamaño": (125, 150),
            },
            "caption": "Sala 2",
            "puertas": {
                "volver": pygame.Rect(100, 400, 70, 40),
                "salida": pygame.Rect(770, 400, 70, 40)
            },
            
            "sala_anterior": "inicio",
            "siguiente_sala": "sala3"
        },
        "sala3": {
            "fondo": "Fondo_sala3.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (100, 400),
                "tamaño": (125, 150),
            },
            "caption": "Sala 3",
            "puertas": {
                "volver": pygame.Rect(100, 400, 70, 40),
                "salida": pygame.Rect(400, 400, 70, 40)
            },
            
            "sala_anterior": "sala2",
            "siguiente_sala": "sala4"
        },
        "sala4": {
            "fondo": "Fondo_sala1.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (400, 400),
                "tamaño": (125, 150),
            },
            "caption": "Sala 3",
            "puertas": {
                "volver": pygame.Rect(400, 400, 70, 40),
                "salida": pygame.Rect(770, 400, 70, 40)
            },
            
            "sala_anterior": "sala3",
            "siguiente_sala": "sala5"
        }
    }
    return configs.get(nombre_sala, None)