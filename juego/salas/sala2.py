import pygame
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlador.rutas import rutas_img
from controlador.cargar_fondos import cargar_fondo
from controlador.colisiones import crear_mascara
from controlador.cargar_personaje import cargar_personaje
from controlador.controles import manejar_mc
from juego.ui.inventory import Inventory, Item

def iniciar_sala2():
    pygame.init()
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escape Del Juicio - Sala 2")

    fuente = pygame.font.SysFont("Arial", 26)
    fondo = cargar_fondo("Fondo_sala1.png", "Fondos", (WIDTH, HEIGHT))
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)
    velocidad = 5

    puntos_hexagono = [
        (132, 411), (980, 411), (1100, 488),
        (1100, 600), (0, 600), (0, 491)
    ]
    mask = crear_mascara(puntos_hexagono, WIDTH, HEIGHT)

    maniquies = []
    posiciones = [
        (850, 250), (910, 400), (730, 340),
        (20, 400), (150, 250), (250, 340)
    ]
    imagenes = ["mm1.png", "mm2.png", "mm3.png", "mm4.png", "mm5.png", "mm6.png"]
    tamaños = [
        (180, 180), (184, 190), (110, 200),
        (110, 200), (110, 200), (186, 200)
    ]

    llave_correcta_index = random.randint(0, len(imagenes) - 1)
    maniquie_malo_index = random.choice([i for i in range(len(imagenes)) if i != llave_correcta_index])

    for idx, (img, pos, (ancho, alto)) in enumerate(zip(imagenes, posiciones, tamaños)):
        maniquie_img, maniquie_rect = cargar_personaje(img, "Michael Myers", WIDTH, HEIGHT)
        maniquie_img = pygame.transform.scale(maniquie_img, (ancho, alto))
        maniquie_rect = maniquie_img.get_rect()
        maniquie_rect.topleft = pos

        hitbox_rect = pygame.Rect(
            maniquie_rect.left + 20,
            maniquie_rect.bottom - 20,
            maniquie_rect.width - 40,
            20
        )

        profundidad = (maniquie_rect.top, maniquie_rect.bottom)

        maniquies.append({
            "img": maniquie_img,
            "rect": maniquie_rect,
            "hitbox": hitbox_rect,
            "profundidad": profundidad,
            "llave_agarrada": False,
            "es_llave_correcta": idx == llave_correcta_index,
            "es_maniqui_malo": idx == maniquie_malo_index
        })

    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False

    mostrar_hitboxes = False
    mensaje_texto = ""
    mensaje_color = (255, 255, 255)
    mensaje_timer = 0

    puerta_interaccion = pygame.Rect(500, 400, 70, 40)

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            inv.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    mostrar_hitboxes = not mostrar_hitboxes

        teclas = pygame.key.get_pressed()
        if not inv.is_open:
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        manejar_mc(personaje_rect, velocidad, inv, mask, [(m["img"], m["rect"], m["hitbox"], m["profundidad"]) for m in maniquies])

        screen.blit(fondo, (0, 0))

        objetos = [(m["img"], m["rect"]) for m in maniquies] + [(personaje, personaje_rect)]
        objetos.sort(key=lambda x: x[1].bottom)
        for img, rect in objetos:
            screen.blit(img, rect)

        mensaje_maniqui = False

        for m in maniquies:
            if personaje_rect.colliderect(m["hitbox"]):
                mensaje_maniqui = True
                llave_existente = any(slot and slot.type == "llave" for slot in inv.inventory_slots + inv.quickbar)

                if m["es_maniqui_malo"]:
                    mensaje_texto = "¡Este maniquí te atacó! Game Over"
                    mensaje_color = (255, 0, 0)
                    pygame.time.delay(1500)
                    iniciar_sala2()
                    return

                if not m["llave_agarrada"]:
                    if not llave_existente:
                        mensaje_texto = "Presiona E para agarrar llave"
                        if teclas[pygame.K_e]:
                            nueva_llave = Item(type="llave", count=1, max_stack=1, color=(255, 215, 0), image=None)
                            for i in range(len(inv.inventory_slots)):
                                if inv.inventory_slots[i] is None:
                                    inv.inventory_slots[i] = nueva_llave
                                    m["llave_agarrada"] = True
                                    break
                    else:
                        mensaje_texto = "Ya tienes una llave en tu inventario"
                else:
                    mensaje_texto = "Ya agarraste la llave de este maniquí"
                break

        pies_personaje = pygame.Rect(
            personaje_rect.centerx - 10,
            personaje_rect.bottom - 5,
            20, 5
        )

        if pies_personaje.colliderect(puerta_interaccion):
            mensaje_maniqui = True
            mensaje_texto = "Usar llave presionando F"
            if teclas[pygame.K_f]:
                llave_existente = next((slot for slot in inv.inventory_slots + inv.quickbar if slot and slot.type == "llave"), None)
                if llave_existente:
                    llave_correcta = any(m["es_llave_correcta"] and m["llave_agarrada"] for m in maniquies)
                    if llave_correcta:
                        pygame.quit()
                        sys.exit()
                    else:
                        mensaje_texto = "Llave incorrecta"
                        mensaje_color = (255, 0, 0)
                        mensaje_timer = 2.0
                        for i in range(len(inv.inventory_slots)):
                            if inv.inventory_slots[i] and inv.inventory_slots[i].type == "llave":
                                inv.inventory_slots[i] = None
                                break
                else:
                    mensaje_texto = "No tienes la llave"
                    mensaje_color = (255, 0, 0)
                    mensaje_timer = 2.0

        if mensaje_maniqui:
            texto = fuente.render(mensaje_texto, True, mensaje_color)
            screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT - 40))

        if mostrar_hitboxes:
            for m in maniquies:
                pygame.draw.rect(screen, (255, 0, 0), m["hitbox"], 1)

        if mensaje_timer > 0:
            mensaje_timer -= dt
        else:
            mensaje_color = (255, 255, 255)

        inv.update(dt)
        inv.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    iniciar_sala2()
