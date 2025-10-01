import sys, os, pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.rutas import rutas_img
from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.colisiones import crear_mascara
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import manejar_mc
from juego.ui.inventory import Inventory

# Importamos la sala dos
from juego.salas.sala2 import iniciar_sala2

def bienvenida_textos(tiempo_actual, tiempo_inicio, fuente, screen, fondo, personaje, personaje_rect):
    mensajes = [
        "Bienvenidos al Escape del Juicio",
        "Este es un juego de vida o muerte en el que te enfrentarás a desafíos mortales",
        "Tendrás que derrotar enemigos, resolver acertijos y escapar con vida",
        "Podrás escapar?"
    ]
    for i, mensaje in enumerate(mensajes):
        if tiempo_actual - tiempo_inicio < (i + 1) * 2000:
            texto_bienvenida = fuente.render(mensaje, True, (255, 255, 255))
            screen.blit(fondo, (0, 0))
            screen.blit(personaje, personaje_rect)
            screen.blit(texto_bienvenida, (screen.get_width() // 2 - texto_bienvenida.get_width() // 2, 600 - 70))
            pygame.display.flip()
            return True
    return False

def iniciar_sala():
    pygame.init()

    # Pantalla fija
    WIDTH, HEIGHT = tamaño_pantallas()
    screen = info_pantalla()

    # Cargar fondo
    fondo_1P = cargar_fondo("Fondo_inicial.png", "Fondos", (WIDTH, HEIGHT))
    fondo_2P = cargar_fondo("Fondo_sala1.png", "Fondos", (WIDTH, HEIGHT))

    # Cargar personaje
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)

    # Puerta
    puerta_interaccion = pygame.Rect(770, 400, 70, 40)
    velocidad = 5

    mask = colision_piso(WIDTH, HEIGHT)
    puntos_hexagono = devolver_puntos_hexagono()

    # --- Crear instancia del inventario ---
    inv = crear_inventario()

    # Inicializar variables para la bienvenida
    mostrar_bienvenida = True
    tiempo_inicio = pygame.time.get_ticks()

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000.0

        if mostrar_bienvenida:
            tiempo_actual = pygame.time.get_ticks()
            if not bienvenida_textos(tiempo_actual, tiempo_inicio, fuente, screen, fondo, personaje, personaje_rect):
                mostrar_bienvenida = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            inv.handle_event(event)

        if not inv.is_open:
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif teclas[pygame.K_F1]:
                mostrar_contorno = not mostrar_contorno
            elif teclas[pygame.K_e]:
                pies_personaje = pygame.Rect(
                    personaje_rect.centerx - 10,
                    personaje_rect.bottom - 5,
                    20, 5
                )
                if pies_personaje.colliderect(puerta_interaccion):
                    # PASAR A SALA 2
                    cargar_sala(fondo_2P, (personaje, personaje_rect), (WIDTH, HEIGHT))  # <-- Aquí pasa a la Sala 2

        # Empty list for maniquies since this room has none
        maniquies = []
        manejar_mc(personaje_rect, velocidad, inv, mask, maniquies)
        inv.update(dt)

        pies_personaje = devolver_pies_personaje(personaje_rect)
        if pies_personaje.colliderect(puerta_interaccion):
            mensaje_paso_sala(screen, (WIDTH, HEIGHT))
       
        # Dibujar contorno del hexágono (solo si debug está activo)
        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)

        mostrar_pantalla()


if __name__ == '__main__':
    iniciar_sala()
