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
from juego.salas.sala2 import iniciar_sala2

# ---------------------------------------------------
# CLASE MAPA EN LA SALA (posicionado en (100,100))
# ---------------------------------------------------
class MapaSala:
    def __init__(self, pos=(100, 100)):
        self.pos = pos

        # Cargar imágenes (ajustá los nombres si tus archivos son distintos)
        self.img_mapa_icono = pygame.image.load("assets/mapa_icono.png").convert_alpha()
        self.img_mapa_icono = pygame.transform.scale(self.img_mapa_icono, (180, 120))
        self.rect_icono = self.img_mapa_icono.get_rect(topleft=pos)

        self.img_mapa_ampliado = pygame.image.load("assets/mapa_ampliado.png").convert_alpha()
        self.img_mapa_ampliado = pygame.transform.scale(self.img_mapa_ampliado, (800, 600))
        self.rect_ampliado = self.img_mapa_ampliado.get_rect(center=(640, 360))

        # Estados
        self.mostrando_ampliado = False
        self.jugador_cerca = False

        # Área de interacción
        self.rect_interaccion = pygame.Rect(
            self.pos[0] - 40, self.pos[1] - 40,
            self.rect_icono.width + 80, self.rect_icono.height + 80
        )

    def actualizar(self, personaje_rect, teclas):
        # Detectar si el jugador está cerca del mapa
        self.jugador_cerca = personaje_rect.colliderect(self.rect_interaccion)

        # Presionar M → abrir/cerrar mapa ampliado
        if self.jugador_cerca and teclas[pygame.K_m]:
            self.mostrando_ampliado = not self.mostrando_ampliado

        # Presionar E → abrir inventario (usa tu lógica actual)
        if self.jugador_cerca and teclas[pygame.K_e]:
            print("Abrir inventario (aquí podrías llamar a tu función)")

    def dibujar(self, pantalla):
        # Dibujar mapa pequeño en la esquina
        pantalla.blit(self.img_mapa_icono, self.rect_icono)

        # Mostrar texto si el jugador está cerca
        if self.jugador_cerca and not self.mostrando_ampliado:
            fuente = pygame.font.Font(None, 28)
            texto = fuente.render("Presiona E (Inventario) / M (Mapa)", True, (255, 255, 255))
            pantalla.blit(texto, (self.pos[0], self.pos[1] - 25))

        # Dibujar mapa ampliado si está activo
        if self.mostrando_ampliado:
            sombra = pygame.Surface(pantalla.get_size(), pygame.SRCALPHA)
            sombra.fill((0, 0, 0, 150))
            pantalla.blit(sombra, (0, 0))
            pantalla.blit(self.img_mapa_ampliado, self.rect_ampliado)
            fuente = pygame.font.Font(None, 32)
            texto = fuente.render("Presiona M para cerrar", True, (255, 255, 255))
            pantalla.blit(texto, (self.rect_ampliado.left + 20, self.rect_ampliado.bottom + 10))


# ---------------------------------------------------
# FUNCIÓN PRINCIPAL DE LA SALA
# ---------------------------------------------------
def iniciar_sala():
    pygame.init()

    # Pantalla fija
    size = tamaño_pantallas()
    screen = info_pantalla()

    # Cargar fondos
    fondo_1P = cargar_fondo("Fondo_inicial.png", "Fondos", size)
    fondo_2P = cargar_fondo("Fondo_sala1.png", "Fondos", size)

    # Cargar personaje
    info_personaje = cargar_personaje("mc_0.png", "mc", size)

    # Puerta de salida
    puerta_interaccion = pygame.Rect(770, 400, 70, 40)
    velocidad = 5

    # Zona jugable
    puntos_hexagono = devolver_puntos_hexagono()
    mask = colision_piso(size)

    mostrar_contorno = False

    # Inventario
    inv = crear_inventario()

    # Crear el mapa en la esquina
    mapa_sala = MapaSala(pos=(100, 100))

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
                    return "sala2"

            # Actualizar el mapa con la posición del jugador y teclas
            mapa_sala.actualizar(info_personaje[1], teclas)

        # Movimiento del personaje
        maniquies = []
        manejar_mc(info_personaje[1], inv, mask, velocidad, maniquies)
        inv.update(dt)

        pies_personaje = devolver_pies_personaje(info_personaje[1])
        if pies_personaje.colliderect(puerta_interaccion):
            mensaje_paso_sala(screen, size)

        # Dibujar todo
        mostrar_pantalla(fondo_1P, info_personaje, screen, inv)

        # Dibujar contorno (debug)
        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)

        # Dibujar el mapa de la sala
        mapa_sala.dibujar(screen)

        pygame.display.flip()


if __name__ == '__main__':
    iniciar_sala()
