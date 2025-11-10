import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.salas.cargar_salas import cargar_sala
from juego.controlador.inventario import crear_inventario

def iniciar_sala3(inv):
    if inv == None:
        inv = crear_inventario()
    return cargar_sala("sala3", maniquies=[], inv=inv)

if __name__ == "__main__":
    iniciar_sala3(crear_inventario())
