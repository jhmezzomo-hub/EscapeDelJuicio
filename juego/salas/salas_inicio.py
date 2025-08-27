import pygame, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controlador.rutas import rutas_img
from controlador.cargar_fondos import cargar_fondo

# Inicializar Pygame
pygame.init()

# Pantalla fija
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sala Jugable con Hexágono en el Piso")

# Cargar fondo
fondo = cargar_fondo(WIDTH, HEIGHT)

# Cargar personaje
path = rutas_img("michael-myers.png")
personaje = pygame.image.load(path)
personaje = pygame.transform.scale(personaje, (120, 200))
personaje_rect = personaje.get_rect(center=(WIDTH//2, HEIGHT - 150))

# Velocidad
velocidad = 5

# ---- CREAR MÁSCARA HEXAGONAL ----
zona_jugable = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
zona_jugable.fill((0, 0, 0, 0))

# Hexágono en el piso (ajusta estos puntos según tu fondo)
p1 = (132, 411)   # arriba izquierda
p2 = (980, 411)   # arriba derecha
p3 = (1100, 488)  # medio derecha
p4 = (1100, 600)  # abajo derecha
p5 = (0, 600)     # abajo izquierda
p6 = (0, 491)     # medio izquierda

puntos_hexagono = [p1, p2, p3, p4, p5, p6]

# Dibujar el polígono en la superficie
pygame.draw.polygon(zona_jugable, (255, 255, 255), puntos_hexagono)

# Crear máscara a partir de la superficie
mask = pygame.mask.from_surface(zona_jugable)

# Bucle principal
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Guardar posición original
    old_pos = personaje_rect.topleft

    # Movimiento
    if keys[pygame.K_w]:
        personaje_rect.y -= velocidad
    if keys[pygame.K_s]:
        personaje_rect.y += velocidad
    if keys[pygame.K_a]:
        personaje_rect.x -= velocidad
    if keys[pygame.K_d]:
        personaje_rect.x += velocidad
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # ---- Verificación de colisión con dos puntos (costados de los pies) ----
    cx_left = personaje_rect.left + 10
    cx_right = personaje_rect.right - 10
    cy = personaje_rect.bottom - 5   # pies

    dentro = False
    if (0 <= cx_left < mask.get_size()[0] and 0 <= cy < mask.get_size()[1] and mask.get_at((cx_left, cy)) != 0) and \
       (0 <= cx_right < mask.get_size()[0] and 0 <= cy < mask.get_size()[1] and mask.get_at((cx_right, cy)) != 0):
        dentro = True

    if not dentro:
        personaje_rect.topleft = old_pos

    # Dibujar fondo
    screen.blit(fondo, (0, 0))

    # Dibujar contorno del hexágono (depuración)
    pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)

    # Dibujar personaje
    screen.blit(personaje, personaje_rect)

    pygame.display.flip()
    clock.tick(60)
