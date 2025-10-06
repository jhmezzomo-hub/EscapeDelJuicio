import sys
import os
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from juego.pantalla.pantalla_inicio import pantalla_de_inicio
from juego.salas.sala2 import iniciar_sala2
from juego.salas.salas_inicio import iniciar_sala_inicio

def main():
    pygame.init()
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pantalla_de_inicio()

    sala_actual = 'sala1'

    while True:
        if sala_actual == 'sala1':
            sala_actual = iniciar_sala_inicio()
        elif sala_actual == 'sala2':
            sala_actual = iniciar_sala2("Fondo_sala1.png", "Fondos")
        else:
            print(f"Error: sala desconocida {sala_actual}")
            break



if __name__ == '__main__':
    main()