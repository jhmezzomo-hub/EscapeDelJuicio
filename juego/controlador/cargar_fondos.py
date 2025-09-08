import pygame

def cargar_fondo(path, size):
    try:
        fondo = pygame.image.load(path)
        fondo = pygame.transform.scale(fondo, size)
        return fondo
    except pygame.error as e:
        print(f"No se pudo cargar el fondo: {path}")
        raise SystemExit(e)