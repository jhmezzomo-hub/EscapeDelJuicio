import pygame
import sys

# (Aquí irían otros imports que necesites, como los de los botones o fondos)

def pantalla_de_inicio():
    # Configuración de la pantalla
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menú Principal")

    # (Aquí cargarías el fondo, los botones, etc.)
    # fondo = ...
    # boton_jugar = ...
    # boton_salir = ...

    # Bucle principal de la pantalla de inicio
    running = True
    while running:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Aquí manejarías los clics en los botones
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if boton_jugar.collidepoint(event.pos):
            #         # Aquí llamarías a la función que inicia el juego principal
            #         print("¡Iniciando juego!") 
            #         running = False # Termina el bucle del menú
            #     if boton_salir.collidepoint(event.pos):
            #         pygame.quit()
            #         sys.exit()

        # Lógica de dibujado
        screen.fill((0, 0, 0)) # Dibuja un fondo negro por ahora

        # (Aquí dibujarías el fondo y los botones)
        # screen.blit(fondo, (0, 0))
        # screen.blit(boton_jugar_img, boton_jugar)
        
        # Actualizar la pantalla
        pygame.display.flip()

    # Al salir del bucle (por ejemplo, al hacer clic en "Jugar"), 
    # la función termina y el control vuelve a main.py.
    # Aquí podrías llamar a la siguiente sala del juego si quisieras.
