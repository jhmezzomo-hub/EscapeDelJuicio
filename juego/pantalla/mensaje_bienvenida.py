import pygame

def bienvenida_textos(tiempo_actual, tiempo_inicio, fuente, screen, fondo):
    mensajes = [
        "Bienvenidos al Escape del Juicio",
        "Este es un juego de vida o muerte en el que te enfrentarás a desafíos mortales",
        "Tendrás que derrotar enemigos, resolver acertijos y escapar con vida",
        "Podrás escapar?"
    ]
    for i, mensaje in enumerate(mensajes):
        if tiempo_actual - tiempo_inicio < (i + 1) * 2000:
            texto_bienvenida = fuente.render(mensaje, True, (255, 255, 255))
            screen.blit(fondo, (0, 0))
            screen.blit(texto_bienvenida, (screen.get_width() // 2 - texto_bienvenida.get_width() // 2, 600 - 70))
            pygame.display.flip()
            return True
    return False