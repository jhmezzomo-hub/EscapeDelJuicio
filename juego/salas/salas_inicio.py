import pygame, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlador.rutas import rutas_img
from controlador.cargar_fondos import cargar_fondo
from controlador.colisiones import crear_mascara, verificar_colision
from controlador.cargar_personaje import cargar_personaje
from controlador.controles import manejar_mc
from juego.ui.inventory import Inventory

def iniciar_sala():
    # Inicializar Pygame
    pygame.init()

    # Pantalla fija
    WIDTH, HEIGHT = 1100, 600
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sala Jugable con Hexágono en el Piso")

    # Cargar fondo
    # Asegúrate de que el nombre del archivo sea el correcto
    fondo = cargar_fondo(rutas_img("Fondo_inicial.png", "Fondos"), (WIDTH, HEIGHT))

    # Cargar personaje
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)

    #Cargar puerta
    puerta = pygame.Rect(725, 220, 180, 180)

    # Velocidad
    velocidad = 5

    # ---- CREAR MÁSCARA HEXAGONAL (usando el controlador) ----
    puntos_hexagono = [
        (132, 411),   # arriba izquierda
        (980, 411),   # arriba derecha
        (1100, 488),  # medio derecha
        (1100, 600),  # abajo derecha
        (0, 600),     # abajo izquierda
        (0, 491)      # medio izquierda
    ]

    mask = crear_mascara(puntos_hexagono, WIDTH, HEIGHT)

    # Flag para mostrar/ocultar el contorno
    mostrar_contorno = False

    # --- Crear instancia del inventario ---
    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False  # empieza cerrado

    # Bucle principal
    clock = pygame.time.Clock()
    corriendo = True
    while corriendo:
        dt = clock.tick(60) / 1000.0

        # RECOGER TODOS LOS EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            inv.handle_event(event)

        if not inv.is_open:
            old_pos = personaje_rect.topleft
            manejar_mc(personaje_rect, velocidad, inv, mask)
            if not verificar_colision(mask, personaje_rect):
                personaje_rect.topleft = old_pos

        inv.update(dt)

        # Dibujar todo
        pantalla.blit(fondo, (0, 0))

        if mostrar_contorno:
            pygame.draw.polygon(pantalla, (0, 255, 0), puntos_hexagono, 2)

        pantalla.blit(personaje, personaje_rect)
        inv.draw(pantalla)

        pygame.display.flip()

# Este bloque permite correr este archivo directamente para probarlo
if __name__ == '__main__':
    iniciar_sala()
