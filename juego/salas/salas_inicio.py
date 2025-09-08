import pygame, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlador.cargar_fondos import cargar_fondo
from controlador.colisiones import crear_mascara
from controlador.cargar_personaje import cargar_personaje
from controlador.controles import manejar_mc
from juego.ui.inventory import Inventory
from controlador.salas import cargar_sala  # <-- Importamos la función de transición

# Inicializar Pygame
pygame.init()

# Pantalla fija
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sala Jugable con Hexágono en el Piso")

# Fuente para mensajes
fuente = pygame.font.SysFont("Arial", 26)

# Cargar fondo
fondo = cargar_fondo(WIDTH, HEIGHT, "Fondo_inicial.png", "Fondos")

# Cargar personaje
personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)

# Rect de la puerta (solo visual)
puerta = pygame.Rect(725, 220, 180, 180)

# Rect más chico para interacción (la base de la puerta)
puerta_interaccion = pygame.Rect(770, 400, 70, 40)

# Velocidad
velocidad = 5

# ---- CREAR MÁSCARA HEXAGONAL ----
puntos_hexagono = [
    (132, 411),
    (980, 411),
    (1100, 488),
    (1100, 600),
    (0, 600),
    (0, 491)
]
mask = crear_mascara(puntos_hexagono, WIDTH, HEIGHT)

mostrar_contorno = False

# --- Inventario ---
inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
inv.is_open = False

# Bucle principal
clock = pygame.time.Clock()
while True:
    dt = clock.tick(60) / 1000.0

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        inv.handle_event(event)

        if not inv.is_open:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_F1:
                    mostrar_contorno = not mostrar_contorno

                # Detectar pies y presionar E
                elif event.key == pygame.K_e:
                    pies_personaje = pygame.Rect(
                        personaje_rect.centerx - 10,
                        personaje_rect.bottom - 5,
                        20, 5
                    )
                    if pies_personaje.colliderect(puerta_interaccion):
                        cargar_sala("Fondo_sala1.png", "Fondos")  # <-- Aquí pasa a la Sala 2

    # Movimiento del personaje
    manejar_mc(personaje_rect, velocidad, inv, mask)

    # Update inventario
    inv.update(dt)

    # Dibujar
    screen.blit(fondo, (0, 0))

    if mostrar_contorno:
        pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)
        pygame.draw.rect(screen, (255, 0, 0), puerta_interaccion, 2)  # debug interacción
        pygame.draw.rect(screen, (0, 0, 255), personaje_rect, 1)      # debug personaje
        pies_personaje = pygame.Rect(
            personaje_rect.centerx - 10,
            personaje_rect.bottom - 5,
            20, 5
        )
        pygame.draw.rect(screen, (0, 255, 255), pies_personaje, 2)     # debug pies

    # Dibujar personaje
    screen.blit(personaje, personaje_rect)

    # Mostrar mensaje solo si los pies tocan la puerta
    pies_personaje = pygame.Rect(
        personaje_rect.centerx - 10,
        personaje_rect.bottom - 5,
        20, 5
    )
    if pies_personaje.colliderect(puerta_interaccion):
        texto = fuente.render("Presiona E para pasar a la siguiente sala", True, (255, 255, 255))
        screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT - 40))

    # Dibujar inventario
    inv.draw(screen)

    pygame.display.flip()
