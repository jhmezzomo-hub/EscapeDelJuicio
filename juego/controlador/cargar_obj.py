import sys, os, pygame
from typing import Dict, Tuple, Any
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_obj_inv import cargar_obj

def cargar_objeto(nombre: str, pos: Tuple[int, int], size_suelo: Tuple[int, int], size_inv: Tuple[int, int]) -> Dict[str, Any]:
    """Carga un objeto para la sala con sus imágenes y propiedades."""
    print(f"\nIniciando carga de objeto: {nombre}")
    print(f"Posición: {pos}, Tamaño suelo: {size_suelo}, Tamaño inv: {size_inv}")
    
    objeto = {
        'nombre': nombre,
        'pos': pos,
        'size_suelo': size_suelo,
        'size_inv': size_inv,
        'visible': True,
        'surf_suelo': None,
        'surf_inv': None,
        'rect': None
    }
    
    img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'img', 'objetos'))
    print(f"Buscando imágenes en: {img_dir}")
    
    # Verificar si los archivos existen antes de cargarlos
    path_suelo = os.path.join(img_dir, f"{nombre}_piso.png")
    path_inv = os.path.join(img_dir, f"{nombre}_inv.png")
    
    if not os.path.exists(path_suelo):
        print(f"ERROR: No se encuentra el archivo: {path_suelo}")
        return objeto
    if not os.path.exists(path_inv):
        print(f"ERROR: No se encuentra el archivo: {path_inv}")
        return objeto
    
    try:
        print(f"Cargando imagen de suelo: {path_suelo}")
        objeto['surf_suelo'] = pygame.image.load(path_suelo).convert_alpha()
        objeto['surf_suelo'] = pygame.transform.scale(objeto['surf_suelo'], size_suelo)
        
        print(f"Cargando imagen de inventario: {path_inv}")
        objeto['surf_inv'] = pygame.image.load(path_inv).convert_alpha()
        objeto['surf_inv'] = pygame.transform.scale(objeto['surf_inv'], size_inv)
        
        objeto['rect'] = objeto['surf_suelo'].get_rect(topleft=pos)
        print(f"Rect creado en posición: {objeto['rect']}")
        
        print("Llamando a cargar_obj...")
        cargar_obj(size_suelo, size_inv, objeto['surf_suelo'], objeto['surf_inv'])
        print(f"Objeto {nombre} cargado exitosamente")
        
    except Exception as e:
        print(f"ERROR al cargar imágenes para {nombre}: {e}")
        print(f"Tipo de error: {type(e)}")
        import traceback
        traceback.print_exc()
    
    return objeto