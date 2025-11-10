import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.salas.cargar_salas import cargar_sala
from juego.controlador.inventario import crear_inventario

def iniciar_sala_3(inv):
    return cargar_sala("sala3", maniquies=[], inv=inv)

if __name__ == "__main__":
    iniciar_sala_3(crear_inventario())
