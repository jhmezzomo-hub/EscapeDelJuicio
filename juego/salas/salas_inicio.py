import sys, os, pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from juego.limite_colisiones.colision_piso import devolver_puntos_hexagono, colision_piso
from juego.controlador.cargar_personaje import cargar_personaje
from juego.salas.cargar_salas import cargar_sala
from juego.controlador.controles import manejar_mc
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from info_pantalla.mostrar_pantalla import mostrar_pantalla
from juego.controlador.inventario import crear_inventario
from juego.controlador.mensaje_paso_sala import mensaje_paso_sala, devolver_pies_personaje
# Importamos la sala dos
from juego.salas.sala2 import iniciar_sala2

def iniciar_sala():
    # Pantalla fija
    size = tamaño_pantallas()
    screen = info_pantalla()

    # Cargar fondo
    fondo = cargar_fondo("Fondo_inicial.png", "Fondos", size)

    # Cargar personaje
    info_personaje = cargar_personaje("mc_0.png", "mc", size)

    # Puerta
    puerta_interaccion = pygame.Rect(770, 400, 70, 40)
    velocidad = 5

    puntos_hexagono = devolver_puntos_hexagono()
    mask = colision_piso(size)

    mostrar_contorno = False

    # --- Crear instancia del inventario ---
    inv = crear_inventario()

    # Inicializar variables para la bienvenida

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000.0

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
                    info_personaje[1].centerx - 10,
                    info_personaje[1].bottom - 5,
                    20, 5
                )
                if pies_personaje.colliderect(puerta_interaccion):
                    # PASAR A SALA 2
                    return "sala2"  # <-- Aquí pasa a la Sala 2

        # Empty list for maniquies since this room has none
        maniquies = []
        manejar_mc(info_personaje[1], inv, mask, velocidad, maniquies)
        inv.update(dt)

        pies_personaje = devolver_pies_personaje(info_personaje[1])
        if pies_personaje.colliderect(puerta_interaccion):
            mensaje_paso_sala(screen, size)
       
        # Dibujar contorno del hexágono (solo si debug está activo)
        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)

        mostrar_pantalla(fondo, info_personaje, screen, inv)


if __name__ == '__main__':
    iniciar_sala()
