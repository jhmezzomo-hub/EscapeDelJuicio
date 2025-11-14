import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.salas.cargar_salas import cargar_sala
from juego.controlador.inventario import crear_inventario

def iniciar_sala3(inv, origen=None):
    if inv is None:
        inv = crear_inventario()
    objetos_sala = []
    # Si viene de sala4, pasar flag especial a cargar_sala
    if origen == "sala4":
        return cargar_sala(
            "sala3",
            maniquies=[],
            inv=inv,
            objetos_sala=objetos_sala,
            puerta_bloqueada=True,
            mensaje_bloqueo="La puerta está bloqueada. Necesitas algo para romperla.",
            origen=origen
        )
    return cargar_sala(
        "sala3",
        maniquies=[],
        inv=inv,
        objetos_sala=objetos_sala,
        puerta_bloqueada=True,
        mensaje_bloqueo="La puerta está bloqueada. Necesitas algo para romperla."
    )

if __name__ == "__main__":
    iniciar_sala3(crear_inventario())
