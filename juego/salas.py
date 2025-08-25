import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mapa estilo Saw Game (isométrico)")

# Colores
COLOR_PARED = (120, 120, 120)
COLOR_PISO = (160, 160, 160)
COLOR_TECHO = (100, 100, 100)
COLOR_LINEA = (0, 0, 0)
COLOR_FONDO = (80, 80, 80)  # <- antes negro, ahora gris

# Cargar personaje y escalarlo
personaje_img = pygame.image.load("michael-myers.png").convert_alpha()
personaje_img = pygame.transform.scale(personaje_img, (100, 200))
personaje_rect = personaje_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

# Velocidad del personaje
velocidad = 5

# Rectángulo de límites (el piso de la sala)
limite_piso = pygame.Rect(200, 500, 600, 100)

# Función para dibujar la sala
def dibujar_sala():
    piso = [(200, 500), (800, 500), (900, 600), (100, 600)]
    pared_izq = [(200, 500), (100, 600), (100, 250), (200, 200)]
    pared_der = [(800, 500), (900, 600), (900, 250), (800, 200)]
    techo = [(200, 200), (800, 200), (900, 250), (100, 250)]

    pygame.draw.polygon(screen, COLOR_PISO, piso)
    pygame.draw.polygon(screen, COLOR_PARED, pared_izq)
    pygame.draw.polygon(screen, COLOR_PARED, pared_der)
    pygame.draw.polygon(screen, COLOR_TECHO, techo)

    pygame.draw.polygon(screen, COLOR_LINEA, piso, 2)
    pygame.draw.polygon(screen, COLOR_LINEA, pared_izq, 2)
    pygame.draw.polygon(screen, COLOR_LINEA, pared_der, 2)
    pygame.draw.polygon(screen, COLOR_LINEA, techo, 2)

# Bucle principal
clock = pygame.time.Clock()
while True:
    # Dibujar fondo gris en vez de negro
    screen.fill(COLOR_FONDO)

    # Dibujar sala
    dibujar_sala()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento con colisiones
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        personaje_rect.y -= velocidad
        if not limite_piso.colliderect(personaje_rect):
            personaje_rect.y += velocidad
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        personaje_rect.y += velocidad
        if not limite_piso.colliderect(personaje_rect):
            personaje_rect.y -= velocidad
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        personaje_rect.x -= velocidad
        if not limite_piso.colliderect(personaje_rect):
            personaje_rect.x += velocidad
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        personaje_rect.x += velocidad
        if not limite_piso.colliderect(personaje_rect):
            personaje_rect.x -= velocidad

    # Dibujar personaje
    screen.blit(personaje_img, personaje_rect)

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)
