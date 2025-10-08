import sys
import os
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from juego.pantalla.pantalla_inicio import pantalla_de_inicio
from juego.controlador.salas import cargar_sala
from juego.controlador.cargar_config import get_config_sala

def main():
    pygame.init()
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pantalla_de_inicio()
    sala_actual = 'inicio'

    while sala_actual:
        config = get_config_sala(sala_actual, screen)
        if config:
            sala_actual = cargar_sala(config)
        else:
            print(f"Error: sala desconocida {sala_actual}")
            break

    pygame.quit()


if __name__ == '__main__':
    main()