import pygame

def devolver_pies_personaje(personaje_rect):
    pies_personaje = pygame.Rect(
        personaje_rect.centerx - 10,
        personaje_rect.bottom - 5,
        20, 5
    )
    return pies_personaje

def mensaje_paso_sala(screen, size):
    # Fuente para mensajes
    fuente = pygame.font.SysFont("Arial", 26)
    # Mostrar mensaje solo si los pies tocan la puerta
    texto = fuente.render("Presiona E para pasar a la siguiente sala", True, (255, 255, 255))
    screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))
