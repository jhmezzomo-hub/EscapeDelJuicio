import sys, os, pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.salas.cargar_salas import cargar_sala



def iniciar_sala_inicio(screen):
    config = {"fondo": "fondo1",
              "nombre_carpeta": "Fondos",
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
