import pygame, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.salas.enfrentamiento import pantalla_de_enfrentamiento
from juego.salas.sala7 import iniciar_sala7

def iniciar_sala6(inv):
    # Aquí iría la lógica específica de la sala 6
    # Por ahora, solo mostramos la pantalla de enfrentamiento
    pantalla_de_enfrentamiento()
    iniciar_sala7()
    return 