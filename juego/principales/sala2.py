# sala2.py
def create_room(ancho=800, alto=600):
    """
    Plantilla de la sala 2: vacía, puerta a la izquierda para volver a la sala 1.
    Devuelve coordenadas en tupla para que main.py cree los pygame.Rect.
    """
    return {
        "barriles": [],
        "paredes": [],
        "puerta": (0, alto // 2, 50, 50),  # puerta a la izquierda (vuelve a sala 1)
        "puerta_extra": (ancho - 80, alto // 2, 40, 60),  # puerta detrás del enemigo
        "fondo": (30, 30, 30),
        "target": 1,
        "target_extra": 3,  # destino de la puerta extra
        "enemigo": (ancho - 100, alto // 2, 50, 50)  # enemigo en sala 2
    }
