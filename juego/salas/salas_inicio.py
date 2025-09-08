import sys, os, pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from juego.limite_colisiones.colision_piso import colision_piso
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import manejar_mc

# Importa la clase Inventory modular (asegurate de tener ui/inventory.py)
from juego.ui.inventory import Inventory

# Inicializar Pygame
pygame.init()

# Pantalla fija
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sala Jugable con Hexágono en el Piso")

# Cargar fondo
fondo = cargar_fondo(WIDTH, HEIGHT)

# Cargar personaje
personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)

#Cargar puerta
puerta = pygame.Rect(725, 220, 180, 180)

# Velocidad
velocidad = 5

mask = colision_piso(WIDTH, HEIGHT)

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
            # otros eventos de la sala que necesiten procesarse aquí...
   
    # Movimiento del personaje: solo si el inventario NO está abierto
    manejar_mc(personaje_rect, velocidad, inv, mask)
    # Update del inventario (por si tenés animaciones/timers)
    inv.update(dt)

    # Dibujar todo
    screen.blit(fondo, (0, 0))

    # Dibujar personaje
    screen.blit(personaje, personaje_rect)

    # Dibujar inventario por encima (solo se muestra si inv.is_open == True dentro de inv.draw)
    inv.draw(screen)

    pygame.display.flip()
