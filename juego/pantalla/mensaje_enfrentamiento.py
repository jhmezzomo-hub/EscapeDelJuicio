import pygame

def enfrentamientos_textos(tiempo_actual, tiempo_inicio, fuente, screen, fondo):
    mensajes = [
        "Enserio creiste que eso era todo?",
        "JAJAJAJAJAJAJAJAJAJAJAJAJAJA",
        "ERES MUY ILUSO",
        "En futbol no te va a ayudar en esta",
        "Tendrás que derrotarme si quieres salir de aquí",
        "Me podras ganar?"
    ]
    for i, mensaje in enumerate(mensajes):
        if tiempo_actual - tiempo_inicio < (i + 1) * 2000:
            texto_bienvenida = fuente.render(mensaje, True, (255, 255, 255))
            screen.blit(fondo, (0, 0))
            screen.blit(texto_bienvenida, (screen.get_width() // 2 - texto_bienvenida.get_width() // 2, 600 - 70))
            pygame.display.flip()
            return True
    return False