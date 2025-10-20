import pygame

def crear_mascara(puntos):
    width = 1100
    height = 600
    superficie = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.polygon(superficie, (255, 255, 255), puntos)
    return pygame.mask.from_surface(superficie)

def verificar_colision(mask, personaje_rect, margen_x=10, margen_y=4):
    cx_left = personaje_rect.left + margen_x
    cx_right = personaje_rect.right - margen_x
    cy = personaje_rect.bottom - margen_y
    width, height = mask.get_size()
    # Si alguna coordenada está fuera de la máscara, consideramos colisión (no transitable)
    if not (0 <= cx_left < width and 0 <= cy < height and 0 <= cx_right < width and 0 <= cy < height):
        return True

    inside_left = mask.get_at((cx_left, cy)) != 0
    inside_right = mask.get_at((cx_right, cy)) != 0

    # Si ambos puntos están dentro de la máscara, NO hay colisión (zona transitable).
    # Colisión ocurre cuando alguno de los puntos está fuera de la zona transitable.
    return not (inside_left and inside_right)

def verificar_colision_maniquies(maniquies, personaje_rect):
    """
    Verifica colisiones entre el personaje y los maniquíes.

    Acepta maniquíes en cualquiera de estos formatos:
      - dict: {"img":..., "rect":..., "hitbox":..., "profundidad":...}
      - tupla/lista: (img, rect, hitbox_rect, profundidad)

    Devuelve True si hay colisión con algún hitbox válido, False en caso contrario.
    La firma es (maniquies, personaje_rect) para mantener compatibilidad con
    llamadas desde `manejar_mc`.
    """
    for m in maniquies:
        # Normalizar campos según el tipo de elemento
        hitbox = None
        profundidad = None
        try:
            if isinstance(m, dict):
                hitbox = m.get("hitbox") or m.get("hitbox_rect")
                profundidad = m.get("profundidad")
            else:
                # tratar secuencia/tupla de longitud variable
                if hasattr(m, "__len__") and len(m) >= 3:
                    hitbox = m[2]
                if hasattr(m, "__len__") and len(m) >= 4:
                    profundidad = m[3]
        except Exception:
            # Si el elemento no es iterable o no tiene los campos esperados,
            # lo ignoramos y continuamos con el siguiente maniquí.
            continue

        if hitbox is None:
            continue

        # Si hay profundidad definida, solo considerar colisión cuando el
        # personaje esté dentro del rango vertical del maniquí.
        if profundidad is not None:
            try:
                y_inicio, y_fin = profundidad
            except Exception:
                # profundidad no en el formato esperado => ignorar restricción
                y_inicio = None
                y_fin = None
        else:
            y_inicio = None
            y_fin = None

        if y_inicio is not None and y_fin is not None:
            if not (y_inicio <= personaje_rect.bottom <= y_fin):
                continue

        if personaje_rect.colliderect(hitbox):
            return True

    return False