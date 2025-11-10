import pygame
import sys
import os
import random
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.salas.cargar_salas import cargar_sala
from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_personaje import cargar_personaje
from juego.pantalla.pantalla_muerte import pantalla_fin
from juego.ui.inventory import Inventory, Item
from juego.controlador.inventario import crear_inventario
from info_pantalla.info_pantalla import info_pantalla, tamaño_pantallas
from juego.controlador.cargar_config import get_config_sala
from juego.controlador.sprites_caminar import sprites_caminar
from limite_colisiones.colision_piso import colision_piso
from juego.controlador.boton_config import crear_boton_config, abrir_menu_config

# ------------------- SALA 2 -------------------
def iniciar_sala2(inv=None):
    random.seed()

    # Si no se pasa un inventario, crear uno nuevo (evita AttributeError)
    if inv is None:
        inv = crear_inventario()

    size = tamaño_pantallas()
    screen = info_pantalla()
    general = get_config_sala("general")

    linterna_encendida = False
    mostrar_mensaje_linterna = True
    timer_mensaje_linterna = 1.0

    maniquies = []
    posiciones = [
        (850, 250), (910, 350), (730, 340),
        (20, 350), (150, 250), (250, 340)
    ]
    imagenes = ["mm1.png", "mm2.png", "mm3.png", "mm4.png", "mm5.png", "mm6.png"]
    tamaños = [
        (180, 180), (184, 190), (110, 200),
        (110, 200), (110, 200), (186, 200)
    ]

    llave_correcta_index = random.randint(0, len(imagenes) - 1)
    maniquie_malo_index = random.randint(0, len(imagenes) - 1)
    while maniquie_malo_index == llave_correcta_index:
        maniquie_malo_index = random.randint(0, len(imagenes) - 1)

    for idx, (img, pos, (ancho, alto)) in enumerate(zip(imagenes, posiciones, tamaños)):
        maniquie_img, maniquie_rect = cargar_personaje(img, "Michael Myers", size, tamaño=(150,200))
        maniquie_img = pygame.transform.scale(maniquie_img, (ancho, alto))
        maniquie_rect = maniquie_img.get_rect()
        maniquie_rect.topleft = pos

        # Calcular hitbox relativa al maniquí de forma más robusta
        hb_width = max(24, maniquie_rect.width - 40)
        hb_height = 30
        hb_x = maniquie_rect.left + (maniquie_rect.width - hb_width) // 2
        # colocar la hitbox cerca de los pies del maniquí
        hb_y = maniquie_rect.bottom - int(hb_height * 1.2)
        hitbox_rect = pygame.Rect(hb_x, hb_y, hb_width, hb_height)

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

    personaje, personaje_rect = general["personaje"], general["personaje_rect"]
    fuente = general["fuente"]

    mostrar_hitboxes = False
    mostrar_malo = False
    mensaje_texto = ""
    mensaje_color = (255, 255, 255)
    mensaje_timer = 0
    linterna_encendida = False
    mostrar_mensaje_linterna = True
    timer_mensaje_linterna = 1.0

    # Crear superficies una sola vez
    oscuridad = pygame.Surface(size, pygame.SRCALPHA)
    
    # Pre-calcular el gradiente de la linterna
    gradiente = pygame.Surface((400, 400), pygame.SRCALPHA)
    for r in range(200, 0, -1):
        alpha = int(255 * (r / 200))
        pygame.draw.circle(gradiente, (0, 0, 0, alpha), (200, 200), r)
    
    # Crear superficie para overlay de maniquí malo
    overlay_malo = pygame.Surface((200, 200), pygame.SRCALPHA)
    overlay_malo.fill((255, 0, 0, 100))
    
    # máscara para colisiones y contraste de piso
    mask = colision_piso(size)

    # Cargar el fondo (una vez)
    fondo = cargar_fondo("fondo_sala1.png", "Fondos")

    # Botón de configuración
    btn_config = crear_boton_config(size[0] - 140, 20)

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0
        teclas = pygame.key.get_pressed()
        # Dibujar el fondo (ya cargado)
        screen.blit(fondo, (0, 0))

        # Actualizar movimiento y animación del personaje y obtener la superficie a dibujar
        current_player_surf = sprites_caminar(size, screen, inv, mask, maniquies, personaje_rect.size, personaje, personaje_rect)

        # Dibujar maniquíes y personaje según profundidad (bottom)
        objetos = [(m["img"], m["rect"]) for m in maniquies] + [(current_player_surf, personaje_rect)]
        objetos.sort(key=lambda x: x[1].bottom)
        for img, rect in objetos:
            screen.blit(img, rect)
        if mostrar_malo:
            for m in maniquies:
                if m["es_maniqui_malo"]:
                    # Usar el overlay pre-creado, escalándolo si es necesario
                    if m["rect"].size != overlay_malo.get_size():
                        overlay_escalado = pygame.transform.scale(overlay_malo, m["rect"].size)
                    else:
                        overlay_escalado = overlay_malo
                    screen.blit(overlay_escalado, m["rect"].topleft)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # manejador del botón de configuración
            try:
                btn_config.handle_event(event, lambda: abrir_menu_config(screen))
            except Exception:
                pass
            inv.handle_event(event)
            # teclas de depuración: F2 = mostrar hitboxes, F3 = resaltar maniquí malo
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                    mostrar_hitboxes = not mostrar_hitboxes
                if event.key == pygame.K_F3:
                    mostrar_malo = not mostrar_malo
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    linterna_encendida = not linterna_encendida
                    if mostrar_mensaje_linterna:
                        mostrar_mensaje_linterna = False
                    mensaje_texto = "Linterna encendida" if linterna_encendida else "Linterna apagada"
                    mensaje_color = (255, 255, 150) if linterna_encendida else (255, 255, 255)
                    mensaje_timer = 2.0

        mensaje_maniqui = False
        mensaje_texto = ""
        mensaje_color = (255, 255, 255)

        pies_personaje = pygame.Rect(personaje_rect.centerx - 10, personaje_rect.bottom - 5, 20, 5)
        if pies_personaje.colliderect(get_config_sala("sala2")["puertas"]["salida"]):
            mensaje_maniqui = True
            mensaje_texto = "Usar llave presionando F"
            if teclas[pygame.K_f]:
                llave_existente = next((slot for slot in inv.inventory_slots + inv.quickbar if slot and slot.type == "llave"), None)
                if llave_existente:
                    llave_correcta = any(m["es_llave_correcta"] and m["llave_agarrada"] for m in maniquies)
                    if llave_correcta:
                        # Pasar a la siguiente sala en lugar de cerrar el juego
                        siguiente = get_config_sala("sala2").get("siguiente_sala")
                        return siguiente
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
        
        # Interacciones con maniquíes (validar colisiones y recoger llaves)
        for m in maniquies:
            if personaje_rect.colliderect(m["hitbox"]):
                mensaje_maniqui = True
                llave_existente = any(slot and slot.type == "llave" for slot in inv.inventory_slots + inv.quickbar)

                if not m["llave_agarrada"]:
                    if not llave_existente:
                        mensaje_texto = "Presiona E para agarrar llave"
                        if teclas[pygame.K_e]:
                            if m["es_maniqui_malo"]:
                                pantalla_fin()
                                iniciar_sala2()
                                return

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

        # Actualizar efecto de linterna (se aplica sobre lo ya dibujado)
        oscuridad.fill((0, 0, 0, 240))
        if linterna_encendida:
            pos = (personaje_rect.centerx - 200, personaje_rect.centery - 200)
            oscuridad.blit(gradiente, pos, special_flags=pygame.BLEND_RGBA_SUB)

        # Blitear la máscara de oscuridad y luego dibujar textos encima
        screen.blit(oscuridad, (0, 0))

        if mostrar_mensaje_linterna:
            alpha = int((math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127)
            texto = fuente.render("Presiona G para prender linterna", True, (255, 255, 150))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))
        elif mensaje_maniqui or mensaje_texto:
            texto = fuente.render(mensaje_texto, True, mensaje_color)
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        # dibujar botón de configuración encima de la escena
        try:
            btn_config.draw(screen)
        except Exception:
            pass

        inv.update(dt)
        inv.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    # Al ejecutar directamente, pasar un inventario creado para evitar errores
    iniciar_sala2(crear_inventario())
