import pygame, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlador.salas import cargar_sala



""""
def bienvenida_textos(tiempo_actual, tiempo_inicio, fuente, screen, fondo, personaje, personaje_rect):
    mensajes = [
        "Bienvenidos al Escape del Juicio",
        "Este es un juego de vida o muerte en el que te enfrentarás a desafíos mortales",
        "Tendrás que derrotar enemigos, resolver acertijos y escapar con vida",
        "Podrás escapar?"
    ]
    for i, mensaje in enumerate(mensajes):
        if tiempo_actual - tiempo_inicio < (i + 1) * 2000:
            texto_bienvenida = fuente.render(mensaje, True, (255, 255, 255))
            screen.blit(fondo, (0, 0))
            screen.blit(personaje, personaje_rect)
            screen.blit(texto_bienvenida, (screen.get_width() // 2 - texto_bienvenida.get_width() // 2, 600 - 70))
            pygame.display.flip()
            return True
    return False
"""
    
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
    