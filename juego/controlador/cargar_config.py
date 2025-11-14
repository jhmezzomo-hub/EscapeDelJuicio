import pygame, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_personaje import cargar_personaje
from info_pantalla.info_pantalla import tamaño_pantallas
from juego.controlador.mensaje_paso_sala import devolver_pies_personaje

def get_config_sala(nombre_sala):
    size = tamaño_pantallas()
    configs = {
        "general": {
            "size": size,
            "screen": pygame.display.get_surface(),
            "personaje":cargar_personaje("mc_0.png", "mc", size, (125, 220))[0],
            "personaje_rect":cargar_personaje("mc_0.png", "mc", size, (125, 220))[1],
            "pies_personaje":devolver_pies_personaje(cargar_personaje("mc_0.png", "mc", size, (125, 220))[1]),
            "fuente":pygame.font.SysFont("Arial", 26),
        },
        "inicio": {
            "fondo": "Fondo_inicial.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                
                "pos_inicial": (100, 400),
                "tamaño": (125, 200),
                "pos_final":(770, 400),
            },
            "puertas": {
                "salida": pygame.Rect(770, 400, 70, 40)
            },
            "items": {
                "papel": pygame.Rect(300, 450, 30, 30)
            },
            "sala_anterior": None,
            "siguiente_sala": "sala2"
        },
        "sala2": {
            "fondo": "Fondo_sala1.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (100, 400),
                "tamaño": (125, 200),
            },
            "puertas": {
                "volver": pygame.Rect(100, 400, 70, 40),
                "salida": pygame.Rect(500, 400, 70, 40)
            },
            
            "sala_anterior": "inicio",
            "siguiente_sala": "sala3"
        },
        "sala3": {
            "fondo": "fondo_puertas3.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (100, 400),
                "tamaño": (125, 200),
            },
            "puertas": {
                "izquierda": pygame.Rect(70, 410, 90, 50),      # Puerta izquierda (arco)
                "salida": pygame.Rect(500, 390, 90, 50),       # Puerta central (arco grande)
                "derecha": pygame.Rect(980, 410, 90, 50)       # Puerta derecha (arco)
            },
            # Si está activado, y la lista de objetos de la sala está VACÍA (o todos fueron recogidos),
            # la puerta izquierda se bloqueará cuando TODOS los objetos de la sala ya estén en el inventario.
            # Esto se usa para la lógica especial de `sala3`.
            "bloquear_si_recolectados": {
                "izquierda": True
            },
            "sala_izquierda": "sala4",
            "sala_derecha": "sala5",
            "salida": "sala6"
        },
        "sala4": {
            "fondo": "fondo_puertaD.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (950, 430),
                "tamaño": (125, 200),
            },
            "puertas": {
                "salida": pygame.Rect(1000, 400, 70, 40)
            },
            "siguiente_sala": "sala3"
        },
        "sala5": {
            "fondo": "Fondo_salaI.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (150, 450),
                "tamaño": (125, 200),
            },
            "puertas": {
                "salida": pygame.Rect(70, 410, 90, 50)
            },
            "siguiente_sala": "sala3"
        },
        "sala6": {
            "fondo": "Fondo_sala1.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (100, 300),
                "tamaño": (125, 200),
            },
            "puertas": {
                "salida": pygame.Rect(400, 400, 70, 40),
            },
            "sala_siguiente": "sala7"
        }
    }
    return configs.get(nombre_sala, None)