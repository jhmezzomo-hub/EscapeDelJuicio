import pygame
import sys
import os
import random
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.verificar_colisiones import crear_mascara
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import manejar_mc
from juego.ui.inventory import Inventory, Item
from info_pantalla.info_pantalla import info_pantalla, tamaño_pantallas

def iniciar_sala2():
    random.seed()  # se resetea la semilla cada vez que inicia el juego

    size = tamaño_pantallas()
    screen = info_pantalla()

    fuente = pygame.font.SysFont("Arial", 26)
    fondo = cargar_fondo("Fondo_sala1.png", "Fondos", size)
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", size)
    velocidad = 5

    puntos_hexagono = [
        (132, 411), (980, 411), (1100, 488),
        (1100, 600), (0, 600), (0, 491)
    ]
    mask = crear_mascara(puntos_hexagono, *size)

    maniquies = []
    posiciones = [
        (850, 250), (910, 450), (730, 340),
        (20, 450), (150, 250), (250, 340)
    ]
    imagenes = ["mm1.png", "mm2.png", "mm3.png", "mm4.png", "mm5.png", "mm6.png"]
    tamaños = [
        (180, 180), (184, 190), (110, 200),
        (110, 200), (110, 200), (186, 200)
    ]

    # Randomización garantizada de los maniquíes
    llave_correcta_index = random.randint(0, len(imagenes) - 1)
    maniquie_malo_index = random.randint(0, len(imagenes) - 1)
    while maniquie_malo_index == llave_correcta_index:
        maniquie_malo_index = random.randint(0, len(imagenes) - 1)

    for idx, (img, pos, (ancho, alto)) in enumerate(zip(imagenes, posiciones, tamaños)):
        maniquie_img, maniquie_rect = cargar_personaje(img, "Michael Myers", size)
        maniquie_img = pygame.transform.scale(maniquie_img, (ancho, alto))
        maniquie_rect = maniquie_img.get_rect()
        maniquie_rect.topleft = pos

        hitbox_rect = pygame.Rect(
            maniquie_rect.left + 20,
            maniquie_rect.bottom - 30 if pos[1] > 250 else maniquie_rect.top - 3,
            maniquie_rect.width - 40,
            30
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

    # Linterna permanente
    linterna_item = Item(type="linterna", count=1, max_stack=1, color=(255, 255, 150), image=None)
    inv.inventory_slots[0] = linterna_item

    mostrar_hitboxes = False
    mensaje_texto = ""
    mensaje_color = (255, 255, 255)
    mensaje_timer = 0
    linterna_encendida = False

    mostrar_mensaje_linterna = True
    timer_mensaje_linterna = 1.0  # segundos

    puerta_interaccion = pygame.Rect(500, 400, 70, 40)

    oscuridad = pygame.Surface(size, pygame.SRCALPHA)
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
                if event.key == pygame.K_g:
                    linterna_encendida = not linterna_encendida
                    if mostrar_mensaje_linterna:
                        mostrar_mensaje_linterna = False
                    mensaje_texto = "Linterna encendida" if linterna_encendida else "Linterna apagada"
                    mensaje_color = (255, 255, 150) if linterna_encendida else (255, 255, 255)
                    mensaje_timer = 2.0

        teclas = pygame.key.get_pressed()
        if not inv.is_open and teclas[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        screen.blit(fondo, (0, 0))
        manejar_mc(personaje_rect, inv, mask, velocidad, maniquies)

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
                    iniciar_sala2()  # ✅ al reiniciar, se vuelve a randomizar
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

        pies_personaje = pygame.Rect(personaje_rect.centerx - 10, personaje_rect.bottom - 5, 20, 5)
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

        if mensaje_timer > 0:
            mensaje_timer -= dt
        else:
            mensaje_color = (255, 255, 255)

        if mostrar_mensaje_linterna:
            timer_mensaje_linterna -= dt
            if timer_mensaje_linterna <= 0:
                mostrar_mensaje_linterna = False

        if mostrar_hitboxes:
            for m in maniquies:
                pygame.draw.rect(screen, (255, 0, 0), m["hitbox"], 1)

        oscuridad.fill((0, 0, 0, 240))
        if linterna_encendida:
            gradiente = pygame.Surface((400, 400), pygame.SRCALPHA)
            for r in range(200, 0, -1):
                alpha = int(255 * (r / 200))
                pygame.draw.circle(gradiente, (0, 0, 0, alpha), (200, 200), r)
            pos = (personaje_rect.centerx - 200, personaje_rect.centery - 200)
            oscuridad.blit(gradiente, pos, special_flags=pygame.BLEND_RGBA_SUB)

        screen.blit(oscuridad, (0, 0))

        if mostrar_mensaje_linterna:
            alpha = int((math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127)
            texto = fuente.render("Presiona G para prender linterna", True, (255, 255, 150))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))
        elif mensaje_maniqui or mensaje_texto:
            texto = fuente.render(mensaje_texto, True, mensaje_color)
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        inv.update(dt)
        inv.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    iniciar_sala2()
