import pygame

def devolver_pies_personaje(personaje_rect):
    # Hitbox de pies de Messi aún más alta y más arriba (global)
    pies_personaje = pygame.Rect(
        personaje_rect.centerx - 40,
        personaje_rect.bottom - 55,
        80, 32
    )
    return pies_personaje

def mensaje_paso_sala(screen, size):
    # Fuente para mensajes
    fuente = pygame.font.SysFont("Arial", 26)
    # Mostrar mensaje solo si los pies tocan la puerta
    texto = fuente.render("Presiona E para pasar a la siguiente sala", True, (255, 255, 255))
    screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))
