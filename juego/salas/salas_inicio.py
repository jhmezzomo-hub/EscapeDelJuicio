import sys, os, pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.salas.cargar_salas import cargar_sala
from juego.controlador.cargar_config import get_config_sala

def iniciar_sala_inicio(screen):
    cargar_sala(get_config_sala("inicio"))
