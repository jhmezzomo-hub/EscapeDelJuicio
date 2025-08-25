import pygame, sys
from rutas import rutas_img

# Inicializar Pygame
pygame.init()

# Dimensiones fijas de la ventana
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sala Isométrica con Colisiones")

# Colores
COLOR_PARED = (120, 120, 120)
COLOR_PISO = (160, 160, 160)
COLOR_TECHO = (100, 100, 100)
COLOR_LINEA = (0, 0, 0)
COLOR_FONDO = (80, 80, 80)

# Cargar personaje
path = rutas_img("michael-myers.png")
personaje_img = pygame.image.load(path).convert_alpha()
personaje_img = pygame.transform.scale(personaje_img, (120, 240))  # más grande
personaje_rect = personaje_img.get_rect(midbottom=(WIDTH // 2, HEIGHT // 2 + 200))

# Física del personaje
velocidad = 7
gravedad = 1
vel_y = 0

# Definir sala en perspectiva
def calcular_limites():
    piso = [(200, 400), (900, 400), (1000, 550), (100, 550)]
    pared_izq = [(200, 400), (100, 550), (100, 150), (200, 100)]
    pared_der = [(900, 400), (1000, 550), (1000, 150), (900, 100)]
    techo = [(200, 100), (900, 100), (1000, 150), (100, 150)]
    return piso, pared_izq, pared_der, techo

def dibujar_sala():
    piso, pared_izq, pared_der, techo = calcular_limites()
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
    screen.fill(COLOR_FONDO)
    dibujar_sala()
    piso, pared_izq, pared_der, techo = calcular_limites()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento lateral
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        personaje_rect.x -= velocidad
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        personaje_rect.x += velocidad
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Gravedad
    vel_y += gravedad
    personaje_rect.y += vel_y

    # Colisiones con límites
    if personaje_rect.left < 100:  # pared izquierda
        personaje_rect.left = 100
    if personaje_rect.right > 1000:  # pared derecha
        personaje_rect.right = 1000
    if personaje_rect.top < 150:  # línea de horizonte (techo inferior)
        personaje_rect.top = 150
        vel_y = 0
    if personaje_rect.bottom > 550:  # piso
        personaje_rect.bottom = 550
        vel_y = 0

    # Dibujar personaje
    screen.blit(personaje_img, personaje_rect)

    pygame.display.flip()
    clock.tick(60)
