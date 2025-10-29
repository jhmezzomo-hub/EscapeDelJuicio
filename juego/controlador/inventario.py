from juego.ui.inventory import Inventory

def crear_inventario():
    # Inventario
    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False
    return inv