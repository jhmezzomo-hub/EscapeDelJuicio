import pygame, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.pantalla.pantalla_inicio import pantalla_de_inicio
from juego.salas.cargar_salas import cargar_sala
from juego.salas.salas_inicio import iniciar_sala_inicio
from juego.salas.sala2 import iniciar_sala2
from juego.salas.sala_mensaje import sala_mensaje_bienvenida
from juego.controlador.inventario import crear_inventario

def main():
    print("Iniciando juego desde main.py...")    
    pygame.init()
    inv = crear_inventario()
    pantalla_de_inicio()  # Mostrar menú principal
    sala_actual = "inicio"
    #sala_mensaje_bienvenida()  # Mostrar mensaje de bienvenida
    while True:
        if sala_actual == "inicio":
            siguiente = iniciar_sala_inicio(inv)
        elif sala_actual == "sala2":
            siguiente = iniciar_sala2(inv)
        elif sala_actual == "sala3":
            siguiente = cargar_sala("sala3")
        elif sala_actual == "sala4":
            siguiente = cargar_sala("sala4")
        else:
            break  # Termina el juego si no hay más salas

        if siguiente is None:
            break  # Termina el juego si la función devuelve None
        sala_actual = siguiente

    print("Juego terminado.")
        # Iniciar el juego si se ejecuta directamente
if __name__ == "__main__":
    main()
    