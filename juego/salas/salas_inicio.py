import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.salas.cargar_salas import cargar_sala
from juego.controlador.cargar_obj import cargar_objeto
from juego.controlador.inventario import crear_inventario

def iniciar_sala_inicio(inv):
    if inv == None:
        inv = crear_inventario()
    
    # Crear objetos de la sala
    print("\nCreando objetos de la sala inicio...")
    objetos = [
        cargar_objeto("papel", (200, 500), (40, 30), (32, 32)),
        cargar_objeto("linterna", (600, 500), (70, 60), (32, 32))
    ]

    # Cargar la sala y pasar los objetos para que se dibujen en el bucle principal
    return cargar_sala("inicio", maniquies=[], inv=inv, objetos_sala=objetos)

if __name__ == "__main__":
    # Al ejecutar directamente, pasar un inventario creado para evitar errores
    iniciar_sala_inicio(crear_inventario())