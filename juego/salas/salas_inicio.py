import sys, os, pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from juego.limite_colisiones.colision_piso import colision_piso, puntos_hexagono
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import manejar_mc

# Importa la clase Inventory modular (asegurate de tener ui/inventory.py)
from juego.ui.inventory import Inventory
from controlador.salas import cargar_sala  # <-- Importamos la función de transición

def iniciar_sala():
    # Inicializar Pygame
    pygame.init()

    # Pantalla fija
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escape Del Juicio")

    # Fuente para mensajes
    fuente = pygame.font.SysFont("Arial", 26)

    # Cargar fondo
    fondo = cargar_fondo("Fondo_inicial.png", "Fondos", (WIDTH, HEIGHT))

    # Cargar personaje
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)

    # Rect de la puerta (solo visual)
    puerta = pygame.Rect(725, 220, 180, 180)

    # Rect más chico para interacción (la base de la puerta)
    puerta_interaccion = pygame.Rect(770, 400, 70, 40)

    # Velocidad
    velocidad = 5

    mask = colision_piso(WIDTH, HEIGHT)
    puntos_hexagono = puntos_hexagono()

    # --- Crear instancia del inventario ---
    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False  # empieza cerrado

    # Bucle principal
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000.0

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Pasar el evento al inventario primero (captura tecla 'I' y clicks si está abierto)
            inv.handle_event(event)

        # Si el inventario está abierto, no procesamos inputs de la sala (salvo que queramos ambos)
        if not inv.is_open:
            presionado = pygame.key.get_pressed()
            if presionado[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif presionado[pygame.K_F1]:
                mostrar_contorno = not mostrar_contorno
            # Detectar pies y presionar E
            elif presionado[pygame.K_e]:
                pies_personaje = pygame.Rect( #Volverlo su propia funcion?
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

        # Dibujar todo
        screen.blit(fondo, (0, 0))

        # Dibujar contorno del hexágono (solo si debug está activo)
        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)

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

        # Dibujar inventario por encima (solo se muestra si inv.is_open == True dentro de inv.draw)
        inv.draw(screen)

        pygame.display.flip()

# Este bloque permite correr este archivo directamente para probarlo
if __name__ == '__main__':
    iniciar_sala()
