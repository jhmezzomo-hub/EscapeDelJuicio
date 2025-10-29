import pygame
import sys
from juego.salas.cargar_salas import cargar_sala
from juego.controlador.cargar_config import get_config_sala


def iniciar_sala2():
    maniquies = []
    cargar_sala("sala2", maniquies)