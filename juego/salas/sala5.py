import pygame, sys, os

# Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from juego.salas.cargar_salas import cargar_sala
from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_config import get_config_sala
from juego.controlador.inventario import crear_inventario
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.cargar_obj import cargar_objeto
from juego.controlador.sprites_caminar import sprites_caminar
from juego.limite_colisiones.colision_piso import colision_piso
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from juego.controlador.boton_config import crear_boton_config, abrir_menu_config
from juego.pantalla.pantalla_muerte import pantalla_fin


def iniciar_sala4(inv):
    if inv is None:
        inv = crear_inventario()
        
    size = tamaño_pantallas()
    screen = info_pantalla()
    general = get_config_sala("general")
    config = get_config_sala("sala4")

    # Cargar el hacha
    objeto_hacha = cargar_objeto("hacha", (800, 350), (60, 80), (40, 40))
    objetos_sala = [objeto_hacha]

    # Cargar a Drácula
    dracula_img, dracula_rect = cargar_personaje("dracula.png", "dracula", size, tamaño=(180, 200))
    dracula_rect.topleft = (850, 340)

    # Línea límite
    limite_x = dracula_rect.left - 10
    punto_inicio = (limite_x - 130, 385)
    punto_fin = (limite_x, size[1])

    # Hitbox de Drácula
    hitbox_dracula = pygame.Rect(
        dracula_rect.left + 20,
        dracula_rect.bottom - 30,
        dracula_rect.width - 40,
        30
    )

    personaje, personaje_rect = general["personaje"], general["personaje_rect"]
    personaje_rect.topleft = config["personaje"]["pos_inicial"]
    fuente = general["fuente"]

    mostrar_hitboxes = True
    mensaje_texto = ""
    mensaje_color = (255, 255, 255)
    mensaje_timer = 0

    mensaje_duracion = 1
    prev_en_puerta = False
    prev_en_dracula = False

    mask = colision_piso(size)
    fondo = cargar_fondo("Fondo_sala1.png", "Fondos")
    btn_config = crear_boton_config(size[0] - 140, 20)
    clock = pygame.time.Clock()
    obstaculos = [{"hitbox": hitbox_dracula}]

    # --- NUEVAS VARIABLES ---
    personaje_bloqueado = False
    temporizador_muerte = 0  # segundos restantes para morir

    while True:
        dt = clock.tick(60) / 1000.0
        teclas = pygame.key.get_pressed()

        # Dibujar fondo
        screen.blit(fondo, (0, 0))

        # Dibujar línea límite antes de los personajes
        if mostrar_hitboxes:
            pygame.draw.line(screen, (255, 0, 0), punto_fin, punto_inicio, 2)

        # Actualizar movimiento, bloqueado si personaje_bloqueado
        current_player_surf = sprites_caminar(size, screen, inv, mask, obstaculos,
                                              personaje_rect.size, personaje, personaje_rect,
                                              disable_movement=personaje_bloqueado)

        # Dibujar objetos, Drácula y personaje
        objetos_para_dibujar = []
        for obj in objetos_sala:
            if obj.get("visible") and obj.get("surf_suelo") and obj.get("rect"):
                objetos_para_dibujar.append((obj["surf_suelo"], obj["rect"]))
        objetos_para_dibujar.extend([(dracula_img, dracula_rect), (current_player_surf, personaje_rect)])
        objetos_para_dibujar.sort(key=lambda x: x[1].bottom)
        for img, rect in objetos_para_dibujar:
            screen.blit(img, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            try:
                btn_config.handle_event(event, lambda: abrir_menu_config(screen))
            except Exception:
                pass
            inv.handle_event(event)

        pies_personaje = pygame.Rect(personaje_rect.centerx - 10, personaje_rect.bottom - 5, 20, 5)
        overlay = pygame.Surface(size, pygame.SRCALPHA)

        # --- OBJETOS INTERACTIVOS ---
        for objeto in objetos_sala:
            if objeto.get("visible") and objeto.get("surf_suelo") and objeto.get("rect"):
                if pies_personaje.colliderect(objeto["rect"]):
                    mensaje = f"Presiona E para recoger {objeto.get('nombre', 'objeto')}"
                    texto = fuente.render(mensaje, True, (255, 255, 255))
                    y_pos = size[1] - 100
                    texto_rect = texto.get_rect(center=(size[0] // 2, y_pos))
                    padding = 10
                    fondo_texto = pygame.Surface(
                        (texto_rect.width + padding * 2, texto_rect.height + padding * 2), pygame.SRCALPHA)
                    fondo_texto.fill((0, 0, 0, 128))
                    overlay.blit(fondo_texto, (texto_rect.x - padding, texto_rect.y - padding))
                    overlay.blit(texto, texto_rect)
                    if teclas[pygame.K_e] and not personaje_bloqueado:
                        try:
                            from juego.controlador.agregar_inv import agregar_a_inventario
                            try:
                                agregar_a_inventario(objeto, inv)
                            except Exception:
                                agregar_a_inventario(inv, objeto)
                        except Exception:
                            pass
                        objeto["visible"] = False

        screen.blit(overlay, (0, 0))

        # --- PUERTA ---
        en_puerta = pies_personaje.colliderect(config["puertas"]["salida"])
        if en_puerta and not prev_en_puerta:
            mensaje_texto = "Presiona E para pasar a la siguiente sala"
            mensaje_timer = mensaje_duracion
        if en_puerta and teclas[pygame.K_e] and not personaje_bloqueado:
            return "siguiente_sala"
        prev_en_puerta = en_puerta

        # --- LÍMITE CON DRÁCULA ---
        px, py = personaje_rect.center
        x1, y1 = punto_inicio
        x2, y2 = punto_fin
        dist = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1) / ((y2 - y1)**2 + (x2 - x1)**2) ** 0.5

        # Si toca la línea, bloquear y activar temporizador
        if not personaje_bloqueado and dist < 10:
            personaje_bloqueado = True
            temporizador_muerte = 1.0  # 1 segundo

        # Si está bloqueado, contar tiempo y morir al cumplirse
        if personaje_bloqueado:
            dracula_img, dracula_rect = cargar_personaje("dracula asustando.png", "dracula", size, tamaño=(180, 200))
            dracula_rect.topleft = (850, 340)
            temporizador_muerte -= dt
            if temporizador_muerte <= 0:
                pantalla_fin()
                return

        # --- INTERACCIÓN CON DRÁCULA ---
        en_dracula = personaje_rect.colliderect(hitbox_dracula)
        if en_dracula and not prev_en_dracula:
            mensaje_texto = "¡Has encontrado a Drácula!"
            mensaje_timer = mensaje_duracion
        prev_en_dracula = en_dracula

        if mensaje_timer > 0:
            mensaje_timer -= dt
            if mensaje_timer <= 0:
                mensaje_texto = ""
        else:
            mensaje_color = (255, 255, 255)

        if mostrar_hitboxes:
            pygame.draw.rect(screen, (255, 0, 0), hitbox_dracula, 1)

        if mensaje_texto:
            texto = fuente.render(mensaje_texto, True, mensaje_color)
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        try:
            btn_config.draw(screen)
        except Exception:
            pass

        inv.update(dt)
        inv.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    iniciar_sala4(crear_inventario())