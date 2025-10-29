from juego.ui.inventory import Inventory

def crear_inventario():
    # Inventario
    inv = Inventory(rows=1, cols=8, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False
    return inv