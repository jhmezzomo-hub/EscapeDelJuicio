import pygame, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.pantalla.pantalla_inicio import pantalla_de_inicio
from juego.salas.cargar_salas import cargar_sala
from juego.salas.sala_mensaje import sala_mensaje_bienvenida
from juego.limite_colisiones.colision_piso import colision_piso

def main():
    print("Iniciando juego desde main.py...")    
    pygame.init()
    pantalla_de_inicio()  # Mostrar menú principal
    sala_actual = "inicio"
    #sala_mensaje_bienvenida()  # Mostrar mensaje de bienvenida

    # Crear máscara de colisiones
    size = (1100, 600)
    mask = colision_piso(size)
    
    while True:
        if sala_actual == "inicio":
            siguiente = cargar_sala("inicio", mask)
        elif sala_actual == "sala2":
            siguiente = cargar_sala("sala2", mask)
        else:
            break  # Termina el juego si no hay más salas

        if siguiente is None:
            break  # Termina el juego si la función devuelve None
        sala_actual = siguiente

    print("Juego terminado.")

if __name__ == "__main__":
    main()