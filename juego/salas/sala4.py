import pygame
import sys
import random
import os

# Añadir el directorio raíz del proyecto al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import teclas_movimiento
from juego.controlador.sprites_caminar import sprites_caminar
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from juego.controlador.cargar_config import get_config_sala
from juego.controlador.inventario import crear_inventario
from juego.controlador.boton_config import crear_boton_config, abrir_menu_config
from juego.ui.inventory import Item
from juego.limite_colisiones.colision_piso import colision_piso
from juego.controlador.cargar_imagen import cargar_img


# ------------------- SALA 4 -------------------
def iniciar_sala4(inv=None):
    """Sala 4: con colisiones, personaje animado y puerta de salida."""
    random.seed()

    # Inventario
    if inv is None:
        inv = crear_inventario()

    # Configuración general
    size = tamaño_pantallas()
    screen = info_pantalla()
    general = get_config_sala("general")
    fuente = general["fuente"]

    # Config de sala 4
    config = get_config_sala("sala4")
    if config is None:
        print("[ERROR] No se encontró configuración para sala4")
        return None

    # Cargar fondo y personaje principal
    fondo = cargar_fondo(config["fondo"], "Fondos")
    personaje, personaje_rect = general["personaje"], general["personaje_rect"]

    # Colisiones del piso + paredes
    mask = colision_piso(size)

    # Botón de configuración
    btn_config = crear_boton_config(size[0] - 140, 20)

    # Variables básicas
    mostrar_contorno = False
    clock = pygame.time.Clock()
    velocidad = 5

    # -------- Puerta de salida (derecha) --------
    puerta_volver = pygame.Rect(size[0] - 100, 320, 80, 120)

    # -------- Cargar personaje (Caperucita) --------
    caperucita_img, caperucita_rect = cargar_personaje("caperucita.png", "caperucita", size, personaje_rect.size)
    caperucita_rect.midbottom = (180, personaje_rect.bottom)

    # -------- Cargar balde y posicionarlo sobre la cabeza de Caperucita --------
    balde_img, balde_rect = cargar_img("balde.png", "balde", size)
    balde_rect.midbottom = (caperucita_rect.centerx, caperucita_rect.top - 40)

    maniquies = []
    print("[DEBUG] Sala 4 cargada correctamente con colisiones y objetos visuales.")

    # Bucle principal
    while True:
        dt = clock.tick(60) / 1000.0

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            try:
                btn_config.handle_event(event, lambda: abrir_menu_config(screen))
            except Exception:
                pass

            inv.handle_event(event)

        # Movimiento del personaje
        if not inv.is_open:
            teclas_movimiento(personaje_rect, velocidad, inv, mask, maniquies)

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif teclas[pygame.K_F1]:
                mostrar_contorno = not mostrar_contorno
            elif teclas[pygame.K_e]:
                # Interacción con la puerta de volver
                if personaje_rect.colliderect(puerta_volver):
                    print("[DEBUG] Volver a sala anterior:", config.get("sala_anterior"))
                    return config.get("sala_anterior")

        # Actualizar inventario
        inv.update(dt)

        # Dibujar fondo
        screen.blit(fondo, (0, 0))

        # Dibujar contornos si están activados
        if mostrar_contorno:
            pygame.draw.rect(screen, (0, 255, 255), personaje_rect, 1)
            pygame.draw.rect(screen, (255, 0, 0), puerta_volver, 2)
            pygame.draw.rect(screen, (255, 255, 0), caperucita_rect, 1)

        # Dibujar personaje principal (animado)
        current_player_surf = sprites_caminar(
            size, screen, inv, mask, maniquies, personaje_rect.size, personaje, personaje_rect
        )

        # Dibujar objetos (balde, Caperucita y jugador)
        if personaje_rect.bottom > caperucita_rect.bottom:
            screen.blit(balde_img, balde_rect)
            screen.blit(current_player_surf, personaje_rect)
            screen.blit(caperucita_img, caperucita_rect)
        else:
            screen.blit(balde_img, balde_rect)
            screen.blit(caperucita_img, caperucita_rect)
            screen.blit(current_player_surf, personaje_rect)

        # Mostrar texto de interacción con la puerta
        if personaje_rect.colliderect(puerta_volver):
            texto = fuente.render("Presiona E para volver a la sala anterior", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        # Dibujar botón de configuración
        try:
            btn_config.draw(screen)
        except Exception:
            pass

        # Dibujar inventario
        try:
            inv.draw(screen)
        except Exception as e:
            print("ERROR al dibujar inventario:", e)

        pygame.display.flip()


if __name__ == "__main__":
    iniciar_sala4(crear_inventario())
