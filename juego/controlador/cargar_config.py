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
            "personaje":cargar_personaje("mc_0.png", "mc", size, (125, 200))[0],
            "personaje_rect":cargar_personaje("mc_0.png", "mc", size, (125, 200))[1],
            "pies_personaje":devolver_pies_personaje(cargar_personaje("mc_0.png", "mc", size, (125, 200))[1]),
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
                "derecha": pygame.Rect(916, 248, 70, 40),
                "izquierda": pygame.Rect(68, 248, 70, 40),
                "salida": pygame.Rect(496, 216, 70, 40)
            },
            
            "sala_anterior": "sala2",
            "sala_izquierda": "sala4",
            "sala_derecha": "sala5"
        },
        "sala4": {
            "fondo": "Fondo_salaD.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (400, 400),
                "tamaño": (125, 200),
            },
            "puertas": {
                "volver": pygame.Rect(400, 400, 70, 40),
                "salida": pygame.Rect(770, 400, 70, 40)
            },
            "siguiente_sala": "sala3"
        },
        "sala5": {
            "fondo": "Fondo_salaI.png",
            "nombre_carpeta": "Fondos",
            "personaje": {
                "pos_inicial": (100, 400),
                "tamaño": (125, 200),
            },
            "puertas": {
                "volver": pygame.Rect(100, 400, 70, 40),
                "salida": pygame.Rect(500, 400, 70, 40)
            },
            "siguiente_sala": "sala3"
        },
    }
    return configs.get(nombre_sala, None)