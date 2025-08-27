import pygame, sys
from rutas import rutas_img

# Inicializar Pygame
pygame.init()

# Pantalla fija en 1100x600
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sala Jugable en el Piso Rojo")

# Cargar fondo (tu imagen de la sala)
path = rutas_img("Fondo_Juego.png")
fondo = pygame.image.load(path)
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

# Cargar personaje
path = rutas_img("michael-myers.png")
personaje = pygame.image.load(path)
personaje = pygame.transform.scale(personaje, (120, 200))
personaje_rect = personaje.get_rect(center=(WIDTH//2, HEIGHT-100))

# Velocidad
velocidad = 5

# Zona jugable (piso rojo)
limite_izq = 0
limite_der = WIDTH
limite_arriba = 260     # horizonte (ajustá si hace falta)
limite_abajo = HEIGHT

# Bucle principal
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Movimiento libre WASD dentro del área del piso rojo
    if keys[pygame.K_w] and personaje_rect.top > limite_arriba:
        personaje_rect.y -= velocidad
    if keys[pygame.K_s] and personaje_rect.bottom < limite_abajo:
        personaje_rect.y += velocidad
    if keys[pygame.K_a] and personaje_rect.left > limite_izq:
        personaje_rect.x -= velocidad
    if keys[pygame.K_d] and personaje_rect.right < limite_der:
        personaje_rect.x += velocidad

    # Dibujar
    screen.blit(fondo, (0, 0))
    screen.blit(personaje, personaje_rect)

    pygame.display.flip()
    clock.tick(60)
