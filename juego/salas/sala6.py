import pygame, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.salas.enfrentamiento import pantalla_de_enfrentamiento
from juego.salas.sala7 import iniciar_sala7

def iniciar_sala6(inv):
    # Aquí iría la lógica específica de la sala 6
    # Por ahora, solo mostramos la pantalla de enfrentamiento
    pantalla_de_enfrentamiento()
    # Esperar a que el jugador presione una tecla o haga click para continuar
    try:
        import pygame, sys
        clock = pygame.time.Clock()
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False
            clock.tick(30)
    except Exception:
        # Si algo falla, no bloquear el juego; continuar a la siguiente sala
        pass
    # Devolver la sala siguiente para que el bucle principal la invoque.
    return 'sala7'

if __name__ == "__main__":
    iniciar_sala6(None)