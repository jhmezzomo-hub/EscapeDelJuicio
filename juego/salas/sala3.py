import pygame
import sys
import os

import pygame.freetype

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.verificar_colisiones import crear_mascara
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import manejar_mc
from juego.ui.inventory import Inventory, Item
from info_pantalla.info_pantalla import info_pantalla, tamaño_pantallas

def iniciar_sala3():
    pygame.init()

    # Configuración básica
    size = tamaño_pantallas()
    screen = info_pantalla()
    clock = pygame.time.Clock()

    # Fondo
    fondo = cargar_fondo("Fondo_sala3.png", "Fondos", size)

    # --- Crear máscara de colisiones con el suelo/paredes ---
    # Podés ajustar los puntos según tu escenario real
    puntos_hexagono = [
        (0, 400), (1200, 400), (1200, 600),
        (0, 600)
    ]
    mask = crear_mascara(puntos_hexagono, *size)

    # --- Cargar personaje principal ---
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", size)
    personaje_rect.midbottom = (size[0] - 120, size[1] - 150)

    # --- Cargar Caperucita ---
    caperucita, caperucita_rect = cargar_personaje("caperucita.png", "Caperucita", size)
    caperucita_rect.midbottom = (160, size[1] - 90)

    # --- Inventario y variables auxiliares ---
    inv = crear_inventario()
    velocidad = 5
    mostrar_colisiones = False
    mensaje_texto = ""
    fuente = pygame.font.SysFont("Arial", 24)
    mensaje_timer = 0.0

    # --- Maniquíes o colisionables ---
    maniquies = [{
        "img": caperucita,
        "rect": caperucita_rect,
        "hitbox": pygame.Rect(caperucita_rect.left + 20, caperucita_rect.bottom - 40, caperucita_rect.width - 40, 40),
        "nombre": "Caperucita"
    }]

    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            inv.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    mostrar_colisiones = not mostrar_colisiones

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # Movimiento con colisiones
        manejar_mc(personaje_rect, inv, mask, velocidad, maniquies)
        inv.update(dt)

        # --- Interacción con Caperucita ---
        mensaje_texto = ""
        pies_personaje = devolver_pies_personaje(personaje_rect)
        for m in maniquies:
            if pies_personaje.colliderect(m["hitbox"]):
                mensaje_texto = "Presiona E para hablar con Caperucita"
                if teclas[pygame.K_e]:
                    mensaje_texto = "Caperucita: ¡Gracias por ayudarme!"
                    mensaje_timer = 2.0

        if mensaje_timer > 0:
            mensaje_timer -= dt
        else:
            mensaje_texto = ""

        # --- Dibujado ---
        screen.blit(fondo, (0, 0))
        screen.blit(caperucita, caperucita_rect)
        screen.blit(personaje, personaje_rect)

        if mostrar_colisiones:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)
            for m in maniquies:
                pygame.draw.rect(screen, (255, 0, 0), m["hitbox"], 1)

        if mensaje_texto:
            texto = fuente.render(mensaje_texto, True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        pygame.display.flip()

if __name__ == "__main__":
    iniciar_sala3()
sa