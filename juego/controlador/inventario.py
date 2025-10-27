from juego.ui.inventory import Inventario

def crear_inventario(ventana):
    """
    Crea una nueva instancia del inventario
    Args:
        ventana: Superficie de pygame donde se dibujará el inventario
    Returns:
        Inventario: Nueva instancia del inventario
    """
    return Inventario(ventana)