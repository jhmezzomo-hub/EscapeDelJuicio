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

    if 0 <= cx_left < mask.get_size()[0] and 0 <= cy < mask.get_size()[1] and \
       0 <= cx_right < mask.get_size()[0] and 0 <= cy < mask.get_size()[1]:
        return mask.get_at((cx_left, cy)) != 0 and mask.get_at((cx_right, cy)) != 0

    return False

def verificar_colision_maniquies(personaje_rect, maniquies):
    for _, _, hitbox_rect in maniquies:
        if personaje_rect.colliderect(hitbox_rect):
            return True
    return False
