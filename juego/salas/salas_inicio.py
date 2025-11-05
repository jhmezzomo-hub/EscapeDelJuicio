import sys, os, pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.salas.cargar_salas import cargar_sala

def iniciar_sala_inicio(inv):
    return cargar_sala("inicio", maniquies=[], inv=inv)
