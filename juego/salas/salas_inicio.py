# salas_inicio.py
import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlador.rutas import rutas_img
from controlador.cargar_fondos import cargar_fondo
from controlador.colisiones import crear_mascara, verificar_colision

# Importa la clase Inventory modular (asegurate de tener ui/inventory.py)
from ui.inventory import Inventory

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
personaje = pygame.image.load(path).convert_alpha()
personaje = pygame.transform.scale(personaje, (120, 200))
personaje_rect = personaje.get_rect(center=(WIDTH//2, HEIGHT - 150))

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
# Ajusta rows/cols/pos si querés (pos es la esquina superior izquierda del UI)
inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
inv.is_open = False  # empieza cerrado

# Si querés cargar íconos reales desde tus rutas, podés hacerlo aquí:
# ej:
# img_path = rutas_img("items/potion.png")
# potion_surf = pygame.image.load(img_path).convert_alpha()
# y en inventory.py adaptar Item para usar surface en vez de .icon

# Bucle principal
clock = pygame.time.Clock()
while True:
    dt = clock.tick(60) / 1000.0

    # RECOGER TODOS LOS EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Pasar el evento al inventario primero (captura tecla 'I' y clicks si está abierto)
        inv.handle_event(event)

        # Si el inventario está abierto, no procesamos inputs de la sala (salvo que queramos ambos)
        if not inv.is_open:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_F1:
                    mostrar_contorno = not mostrar_contorno  # alternar debug
            # otros eventos de la sala que necesiten procesarse aquí...

    # Movimiento del personaje: solo si el inventario NO está abierto
    keys = pygame.key.get_pressed()
    old_pos = personaje_rect.topleft
    if not inv.is_open:
        if keys[pygame.K_w]:
            personaje_rect.y -= velocidad
        if keys[pygame.K_s]:
            personaje_rect.y += velocidad
        if keys[pygame.K_a]:
            personaje_rect.x -= velocidad
        if keys[pygame.K_d]:
            personaje_rect.x += velocidad

        # ---- Verificación de colisión ----
        if not verificar_colision(mask, personaje_rect):
            personaje_rect.topleft = old_pos

    # Update del inventario (por si tenés animaciones/timers)
    inv.update(dt)

    # Dibujar todo
    screen.blit(fondo, (0, 0))

    # Dibujar contorno del hexágono (solo si debug está activo)
    if mostrar_contorno:
        pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)

    # Dibujar personaje
    screen.blit(personaje, personaje_rect)

    # Dibujar inventario por encima (solo se muestra si inv.is_open == True dentro de inv.draw)
    inv.draw(screen)

    pygame.display.flip()
