import sys, os, pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from juego.limite_colisiones.colision_piso import colision_piso, devolver_puntos_hexagono
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import manejar_mc
from juego.controlador.inventario import crear_inventario
from juego.controlador.cargar_salas import cargar_sala  # <-- Importamos la función de transición
from info_pantalla.info_pantalla import info_pantalla, tamaño_pantallas
from info_pantalla.mostrar_pantalla import mostrar_pantalla
from juego.controlador.mensaje_paso_sala import mensaje_paso_sala, devolver_pies_personaje
def iniciar_sala():
    # Inicializar Pygame
    pygame.init()

    # Pantalla fija
    WIDTH, HEIGHT = tamaño_pantallas()
    screen = info_pantalla()

    # Cargar fondo
    fondo_1P = cargar_fondo("Fondo_inicial.png", "Fondos", (WIDTH, HEIGHT))
    fondo_2P = cargar_fondo("Fondo_sala1.png", "Fondos", (WIDTH, HEIGHT))

    # Cargar personaje
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)

    # Rect de la puerta (solo visual)
    puerta = pygame.Rect(725, 220, 180, 180)

    # Rect más chico para interacción (la base de la puerta)
    puerta_interaccion = pygame.Rect(770, 400, 70, 40)

    # Velocidad
    velocidad = 5

    mask = colision_piso(WIDTH, HEIGHT)
    puntos_hexagono = devolver_puntos_hexagono()

    # --- Crear instancia del inventario ---
    inv = crear_inventario()

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
                    cargar_sala(fondo_2P, (personaje, personaje_rect), (WIDTH, HEIGHT))  # <-- Aquí pasa a la Sala 2
        # Movimiento del personaje
        manejar_mc(personaje_rect, velocidad, inv, mask)
        # Update inventario
        inv.update(dt)

        pies_personaje = devolver_pies_personaje(personaje_rect)
        if pies_personaje.colliderect(puerta_interaccion):
            mensaje_paso_sala(screen, (WIDTH, HEIGHT))
       
        # Dibujar contorno del hexágono (solo si debug está activo)
        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)

        mostrar_pantalla()

# Este bloque permite correr este archivo directamente para probarlo
if __name__ == '__main__':
    iniciar_sala()
