import pygame, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlador.rutas import rutas_img
from controlador.cargar_fondos import cargar_fondo
from controlador.colisiones import crear_mascara, verificar_colision
from controlador.cargar_personaje import cargar_personaje
from controlador.controles import manejar_mc
from juego.ui.inventory import Inventory
from controlador.salas import cargar_sala  # <-- Importamos la función de transición
from juego.salas.sala2 import iniciar_sala2

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
    puerta_interaccion = pygame.Rect(770, 400, 120, 40)

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

    # --- Variables para mostrar mensaje de bienvenida ---
    mostrar_bienvenida = True
    tiempo_inicio = pygame.time.get_ticks()

    # --- Crear instancia del inventario ---
    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False  # empieza cerrado

    # Bucle principal
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000.0

        # Mostrar mensaje de bienvenida los primeros 2 segundos
        if mostrar_bienvenida:
            lista_textos = [
                "Bienvenidos al Escape del Juicio",
                "Este es un juego de vida o muerte en el que te enfrentarás a desafíos mortales",
                "Tendrás que derrotar enemigos, resolver acertijos y escapar con vida",
                "¿Podrás escapar?"
            ]
            """tiempo_actual = pygame.time.get_ticks()
            screen.blit(fondo, (0, 0))
            for i, texto in enumerate(lista_textos):
                if tiempo_actual - tiempo_inicio < (i + 1) * 2000:
                    texto_bienvenida = fuente.render(texto, True, (255, 255, 255))
                    screen.blit(personaje, personaje_rect)
                    screen.blit(texto_bienvenida, (WIDTH // 2 - texto_bienvenida.get_width() // 2, 600 - 70))
                    pygame.display.flip()
                    break"""
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_inicio < 2000:
                texto_bienvenida = fuente.render("Bienvenidos al Escape del Juicio", True, (255, 255, 255))
                screen.blit(fondo, (0, 0))
                screen.blit(personaje, personaje_rect)
                screen.blit(texto_bienvenida, (WIDTH // 2 - texto_bienvenida.get_width() // 2, 600 - 70))
                pygame.display.flip()
                continue
            if tiempo_actual - tiempo_inicio < 4000:
                texto_bienvenida2 = fuente.render("Este es un juego de vida o muerte en el que te enfrentarás a desafíos mortales", True, (255, 255, 255))
                screen.blit(fondo, (0, 0))
                screen.blit(personaje, personaje_rect)
                screen.blit(texto_bienvenida2, (WIDTH // 2 - texto_bienvenida2.get_width() // 2, 600 - 70))
                pygame.display.flip()
                continue
            if tiempo_actual - tiempo_inicio < 6000:
                texto_bienvenida2 = fuente.render("Tendrás que derrotar enemigos, resolver acertijos y escapar con vida", True, (255, 255, 255))
                screen.blit(fondo, (0, 0))
                screen.blit(personaje, personaje_rect)
                screen.blit(texto_bienvenida2, (WIDTH // 2 - texto_bienvenida2.get_width() // 2, 600 - 70))
                pygame.display.flip()
                continue
            if tiempo_actual - tiempo_inicio < 8000:
                texto_bienvenida2 = fuente.render("Podrás escapar?", True, (255, 255, 255))
                screen.blit(fondo, (0, 0))
                screen.blit(personaje, personaje_rect)
                screen.blit(texto_bienvenida2, (WIDTH // 2 - texto_bienvenida2.get_width() // 2, 600 - 70))
                pygame.display.flip()
                continue
            else:
                mostrar_bienvenida = False

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
                    iniciar_sala2()  # <-- Aquí pasa a la Sala 2

        # Movimiento del personaje
        manejar_mc(personaje_rect, velocidad, inv, mask)
        # Update inventario
        inv.update(dt)

        # Dibujar todo
        screen.blit(fondo, (0, 0))

        # Dibujar contorno del hexágono (solo si debug está activo)
        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)
            pygame.draw.rect(screen, (255, 0, 0), puerta_interaccion, 2)  # debug interacción
            pygame.draw.rect(screen, (0, 0, 255), personaje_rect, 1)      # debug personaje
            pies_personaje = pygame.Rect(
                personaje_rect.centerx - 10,
                personaje_rect.bottom - 5,
                20, 5
            )
            pygame.draw.rect(screen, (0, 255, 255), pies_personaje, 2)     # debug pies

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


def esenciales():
    esenciales = [inv, personaje, personaje_rect, fondo, mask]
    return esenciales

# Este bloque permite correr este archivo directamente para probarlo
if __name__ == '__main__':
    iniciar_sala()
