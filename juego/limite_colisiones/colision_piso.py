from juego.limite_colisiones.crear_mascara import crear_mascara

def colision_piso(WIDTH, HEIGHT):
    # ---- CREAR MÁSCARA HEXAGONAL (usando el controlador) ----
    puntos_hexagono = [
        (132, 411),   # arriba izquierda
        (980, 411),   # arriba derecha
        (1100, 488),  # medio derecha
        (1100, 600),  # abajo derecha
        (0, 600),     # abajo izquierda
        (0, 491)      # medio izquierda
    ]
    mask = crear_mascara(puntos_hexagono, WIDTH, HEIGHT)
    return mask