import sys, os, pygame
from typing import Dict, Tuple, Any
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.ui.inventory import Item

def agregar_a_inventario(objeto: Dict[str, Any], inv) -> bool:
    """Intenta agregar un objeto al inventario del jugador."""
    if not objeto['visible']:
        return False
    
    try:
        if hasattr(inv, "inventory_slots"):
            for i in range(len(inv.inventory_slots)):
                if inv.inventory_slots[i] is None:
                    inv.inventory_slots[i] = Item(
                        type=objeto['nombre'],
                        count=1,
                        max_stack=1,
                        color=(255, 255, 255),
                        image=objeto['surf_inv']
                    )
                    objeto['visible'] = False
                    return True
    except Exception as e:
        print(f"Error al agregar {objeto['nombre']} al inventario: {e}")
    return False