import pygame

def mostrar_pantalla(fondo, personaje_info, screen, inv):
    screen.blit(fondo, (0, 0))
    screen.blit(personaje_info[0], personaje_info[1])
    inv.draw(screen)
    pygame.display.flip()