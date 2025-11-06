import pygame

def cargar_obj(obj_size = None, obj_inv_size = None, obj_surf = None, obj_inv_surf = None):
    if obj_surf is None:
            obj_surf = pygame.Surface(obj_size, pygame.SRCALPHA)
            obj_surf.fill((200, 200, 100))  # Color amarillento para la linterna
            pygame.draw.rect(obj_surf, (150, 150, 50), obj_surf.get_rect(), 1)
    else:
        try:
            obj_surf = pygame.transform.smoothscale(obj_surf, obj_size)
        except Exception:
            obj_surf = pygame.transform.scale(obj_surf, obj_size)

    # Crear/escalar imagen de linterna en inventario
    if obj_inv_surf is None:
        obj_inv_surf = obj_surf.copy()
    else:
        try:
            obj_inv_surf = pygame.transform.smoothscale(obj_inv_surf, obj_inv_size)
        except Exception:
            obj_inv_surf = pygame.transform.scale(obj_inv_surf, obj_inv_size)

    