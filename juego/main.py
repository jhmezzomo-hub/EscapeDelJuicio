import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.salas.salas_inicio import iniciar_sala
from juego.pantalla.pantalla_inicio import pantalla_de_inicio
from juego.salas.sala2 import iniciar_sala2

def main():
    print("Iniciando juego desde main.py...")
    pantalla_de_inicio()  # Mostrar menú principal
    iniciar_sala()        # Solo se ejecuta después de salir del menú
    print("Juego terminado.")

if __name__ == '__main__':
    main()