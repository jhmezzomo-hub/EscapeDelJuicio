
def verificar_colision(mask, personaje_rect, margen_x=10, margen_y=4):
    """
    Verifica si el personaje está dentro de la máscara usando dos puntos en los pies.
    - mask: máscara de la zona jugable
    - personaje_rect: rectángulo del personaje
    - margen_x: ajuste lateral de los pies
    - margen_y: ajuste en la parte inferior del personaje
    Devuelve True si está dentro, False si no.
    """
    cx_left = personaje_rect.left + margen_x
    cx_right = personaje_rect.right - margen_x
    cy = personaje_rect.bottom - margen_y

    # Verificar dentro de los límites
    if 0 <= cx_left < mask.get_size()[0] and 0 <= cy < mask.get_size()[1] and \
       0 <= cx_right < mask.get_size()[0] and 0 <= cy < mask.get_size()[1]:
        return (mask.get_at((cx_left, cy)) != 0 and mask.get_at((cx_right, cy)) != 0)
    
    return False
