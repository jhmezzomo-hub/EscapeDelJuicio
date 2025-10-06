import sys, os, pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from juego.limite_colisiones.colision_piso import devolver_puntos_hexagono, colision_piso
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.cargar_salas import cargar_sala
from juego.controlador.controles import manejar_mc
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from info_pantalla.mostrar_pantalla import mostrar_pantalla
from juego.controlador.inventario import crear_inventario
from juego.controlador.mensaje_paso_sala import mensaje_paso_sala, devolver_pies_personaje
# Importamos la sala dos
from juego.salas.sala2 import iniciar_sala2

def bienvenida_textos(tiempo_actual, tiempo_inicio, fuente, screen, fondo, info_personaje):
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
            screen.blit(info_personaje)
            screen.blit(texto_bienvenida, (screen.get_width() // 2 - texto_bienvenida.get_width() // 2, 600 - 70))
            pygame.display.flip()
            return True
    return False

def iniciar_sala():
    pygame.init()

    # Pantalla fija
    size = tamaño_pantallas()
    screen = info_pantalla()

    # Cargar fondo
    fondo_1P = cargar_fondo("Fondo_inicial.png", "Fondos", size)
    fondo_2P = cargar_fondo("Fondo_sala1.png", "Fondos", size)

    # Cargar personaje
    info_personaje = cargar_personaje("mc_0.png", "mc", size)

    # Puerta
    puerta_interaccion = pygame.Rect(770, 400, 70, 40)
    velocidad = 5

    puntos_hexagono = devolver_puntos_hexagono()
    mask = colision_piso(puntos_hexagono, size)


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
            if not bienvenida_textos(tiempo_actual, tiempo_inicio, pygame.font.SysFont("Arial", 26), screen, fondo_1P, info_personaje):
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
                    info_personaje[1].centerx - 10,
                    info_personaje[1].bottom - 5,
                    20, 5
                )
                if pies_personaje.colliderect(puerta_interaccion):
                    # PASAR A SALA 2
                    cargar_sala(fondo_2P, info_personaje, size)  # <-- Aquí pasa a la Sala 2

        # Empty list for maniquies since this room has none
        maniquies = []
        manejar_mc(info_personaje[1], velocidad, inv, mask, maniquies)
        inv.update(dt)

        pies_personaje = devolver_pies_personaje(info_personaje[1])
        if pies_personaje.colliderect(puerta_interaccion):
            mensaje_paso_sala(screen, size)
       
        # Dibujar contorno del hexágono (solo si debug está activo)
        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)

        mostrar_pantalla()


if __name__ == '__main__':
    iniciar_sala()
