import pygame, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlador.salas import cargar_sala



def iniciar_sala_inicio(screen):
    config = {"fondo": "fondo1",
              "nombre_carpeta": "Fondos",
              "WIDTH": 1100,
              "HEIGHT": 600,
              "personaje": {
                  "pos_inicial":(100, 400),
                  "tamaño": (50, 70),
                  "velocidad": 5
              },
              "personaje"
              "caption": "Escape Del Juicio",
              "screen": screen,
              "puertas": 
                    {
                        "salida": pygame.Rect(770, 400, 70, 40)
                    }
             }
    
    
    cargar_sala(config)
