import pygame, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.pantalla.pantalla_inicio import pantalla_de_inicio
from juego.salas.salas_inicio import iniciar_sala
from juego.salas.sala2 import iniciar_sala2
from juego.salas.sala_mensaje import sala_mensaje_bienvenida

def main():
    print("Iniciando juego desde main.py...")
    pantalla_de_inicio()  # Mostrar menú principal
    sala_actual = "sala1"
    sala_mensaje_bienvenida()  # Mostrar mensaje de bienvenida
    while True:
        if sala_actual == "sala1":
            siguiente = iniciar_sala()
        elif sala_actual == "sala2":
            siguiente = iniciar_sala2()
        else:
            break  # Termina el juego si no hay más salas

        if siguiente is None:
            break  # Termina el juego si la función devuelve None
        sala_actual = siguiente

    print("Juego terminado.")
        # Iniciar el juego si se ejecuta directamente
if __name__ == "__main__":
    main()