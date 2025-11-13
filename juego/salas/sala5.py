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
    # control de si el límite está activo (permite bloqueo)
    limite_activo = True

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
    fondo = cargar_fondo("fondo_puertaI.png", "Fondos")
    btn_config = crear_boton_config(size[0] - 140, 20)
    clock = pygame.time.Clock()
    obstaculos = [{"hitbox": hitbox_dracula}]

    # --- NUEVAS VARIABLES ---
    personaje_bloqueado = False
    temporizador_muerte = 0  # segundos restantes para morir

    # --- Estado del ajo / animación ---
    ajo_animando = False
    ajo_timer = 0.0
    ajo_duracion = 0.8
    ajo_surf = None
    ajo_rect = None
    ajo_usado = False

    # Estado de Drácula resguardado/desaparecido
    dracula_resguardado_activo = False
    dracula_resguardado_timer = 0.0
    dracula_visible = True
    # intentar cargar imagen alternativa de Drácula resguardado
    try:
        dracula_resguardado_img, _ = cargar_personaje("dracula_resguardado.png", "dracula_resguardado", size, tamaño=(180,200))
    except Exception:
        dracula_resguardado_img = None

    # Helpers para inventario: detectar ajo y remover ajo (varias APIs)
    def inv_tiene_ajo(inv_obj):
        try:
            # varios métodos posibles
            for m in ("tiene", "has_item", "contains"):
                if hasattr(inv_obj, m):
                    try:
                        if getattr(inv_obj, m)("ajo"):
                            return True
                    except Exception:
                        pass
            # listas comunes
            for attr in ("items", "objetos", "inventario", "slots", "contenidos"):
                if hasattr(inv_obj, attr):
                    lst = getattr(inv_obj, attr)
                    try:
                        for it in lst:
                            if isinstance(it, dict):
                                nombre = (it.get("nombre") or it.get("name") or "")
                                if "ajo" in nombre.lower():
                                    return True
                            elif isinstance(it, str):
                                if "ajo" in it.lower() or it.lower() == "garlic":
                                    return True
                    except Exception:
                        pass
            # check textual representation
            try:
                if "ajo" in str(inv_obj).lower():
                    return True
            except Exception:
                pass
        except Exception:
            pass
        return False

    def inv_quitar_ajo(inv_obj):
        try:
            for m in ("quitar", "remove", "remove_item", "eliminar"):
                if hasattr(inv_obj, m):
                    try:
                        getattr(inv_obj, m)("ajo")
                        return True
                    except Exception:
                        try:
                            getattr(inv_obj, m)({"nombre":"ajo"})
                            return True
                        except Exception:
                            pass
            for attr in ("items", "objetos", "inventario", "slots", "contenidos"):
                if hasattr(inv_obj, attr):
                    lst = getattr(inv_obj, attr)
                    try:
                        for i, it in enumerate(list(lst)):
                            name = ""
                            if isinstance(it, dict):
                                name = it.get("nombre") or it.get("name") or ""
                            elif isinstance(it, str):
                                name = it
                            if "ajo" in name.lower():
                                try:
                                    lst.pop(i)
                                except Exception:
                                    try:
                                        lst.remove(it)
                                    except Exception:
                                        pass
                                return True
                    except Exception:
                        pass
        except Exception:
            pass
        return False

    # Intento de cargar un surf de ajo (si existe como objeto). Fallback dibujable más abajo.
    try:
        ajo_test_surf, _ = cargar_objeto("ajo", (0,0), (24,24), (12,12))
        ajo_surf = ajo_test_surf
    except Exception:
        ajo_surf = None

    while True:
        dt = clock.tick(60) / 1000.0
        teclas = pygame.key.get_pressed()

        # Dibujar fondo
        screen.blit(fondo, (0, 0))

        # Dibujar línea límite antes de los personajes
        if mostrar_hitboxes and limite_activo:
            pygame.draw.line(screen, (255, 0, 0), punto_fin, punto_inicio, 2)

        # Actualizar movimiento, bloqueado si personaje_bloqueado
        current_player_surf = sprites_caminar(size, screen, inv, mask, obstaculos,
                                              personaje_rect.size, personaje, personaje_rect,
                                              disable_movement=personaje_bloqueado)

        # Si está bloqueado, contar tiempo y morir al cumplirse
        if personaje_bloqueado:
            dracula_img, dracula_rect = cargar_personaje("dracula asustando.png", "dracula", size, tamaño=(180, 200))
            dracula_rect.topleft = (850, 340)
            
            personaje_asustado, _ = cargar_personaje("mc_asustado.png", "mc", size, personaje_rect.size)
            personaje_asustado = pygame.transform.flip(personaje_asustado, personaje_rect.centerx < dracula_rect.centerx, False)
            current_player_surf = personaje_asustado
            personaje_rect.topleft = personaje_rect.topleft
            temporizador_muerte -= dt
            if temporizador_muerte <= 0:
                pantalla_fin()
                return

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

        # Detectar si el inventario está "abierto"
        inv_abierto = False
        try:
            if hasattr(inv, "abierto"):
                inv_abierto = bool(getattr(inv, "abierto"))
            elif hasattr(inv, "open"):
                inv_abierto = bool(getattr(inv, "open"))
            elif hasattr(inv, "is_open"):
                inv_abierto = bool(getattr(inv, "is_open"))
            elif hasattr(inv, "visible"):
                inv_abierto = bool(getattr(inv, "visible"))
            else:
                inv_abierto = "abierto" in str(inv).lower() or "open" in str(inv).lower()
        except Exception:
            inv_abierto = False

        # Si está bloqueado por la línea y tenemos ajo y el inventario está abierto,
        # permitir presionar E para usar el ajo desde el inventario
        if personaje_bloqueado and limite_activo and inv_tiene_ajo(inv) and inv_abierto and not ajo_animando and not dracula_resguardado_activo:
            # indicación en pantalla
            try:
                texto = fuente.render("Presiona E sobre el ajo para usarlo", True, (255,255,255))
                screen.blit(texto, (size[0]//2 - texto.get_width()//2, size[1] - 80))
            except Exception:
                pass
            if teclas[pygame.K_e]:
                # remover del inventario, intentar cerrar inventario
                inv_quitar_ajo(inv)
                # intentar cerrar gui del inventario por varios nombres
                for m in ("close","cerrar","cerrar_inventario"):
                    if hasattr(inv, m):
                        try:
                            getattr(inv, m)()
                        except Exception:
                            pass
                try:
                    if hasattr(inv, "abierto"):
                        setattr(inv, "abierto", False)
                    if hasattr(inv, "visible"):
                        setattr(inv, "visible", False)
                except Exception:
                    pass
                # iniciar animación del ajo
                ajo_animando = True
                ajo_timer = 0.0
                ajo_usado = True
                # crear surf si no existe
                if ajo_surf is None:
                    ajo_surf = pygame.Surface((24,24), pygame.SRCALPHA)
                    try:
                        pygame.draw.circle(ajo_surf, (220,220,60), (12,12), 10)
                    except Exception:
                        pass
                ajo_rect = ajo_surf.get_rect(center=personaje_rect.center)
                # permitir mover durante animación si se desea; bloquear tiempo de muerte
                personaje_bloqueado = False

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
        if limite_activo and not personaje_bloqueado and dist < 10:
            personaje_bloqueado = True
            temporizador_muerte = 5.0  # 5 segundos

        
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

        # Mostrar temporizador grande y visible cuando el personaje está bloqueado
        if personaje_bloqueado:
            tiempo_mostrar = max(0.0, temporizador_muerte)
            texto_temp = fuente.render(f"{tiempo_mostrar:.1f}s", True, (255, 50, 50))
            rect_temp = texto_temp.get_rect(center=(size[0] // 2, size[1] // 2 - 40))
            fondo_temp = pygame.Surface((rect_temp.width + 20, rect_temp.height + 20), pygame.SRCALPHA)
            fondo_temp.fill((0, 0, 0, 160))
            screen.blit(fondo_temp, (rect_temp.x - 10, rect_temp.y - 10))
            screen.blit(texto_temp, rect_temp)

        # --- ACTUALIZAR ANIMACIÓN DEL AJO ---
        if ajo_animando and ajo_surf and ajo_rect:
            ajo_timer += dt
            t = min(1.0, ajo_timer / ajo_duracion)
            try:
                start = personaje_rect.center
                end = dracula_rect.center
                ajo_rect.center = (int(start[0] + (end[0]-start[0])*t), int(start[1] + (end[1]-start[1])*t))
            except Exception:
                pass
            # dibujar ajo por encima
            try:
                screen.blit(ajo_surf, ajo_rect)
            except Exception:
                pass
            if t >= 1.0:
                # efecto: Drácula resguardado, mensaje, desaparecer y quitar línea
                mensaje_texto = "¡Mejor me voy!"
                mensaje_timer = 2.5
                dracula_resguardado_activo = True
                dracula_resguardado_timer = 2.5
                limite_activo = False
                mostrar_hitboxes = False
                ajo_animando = False
                try:
                    ajo_surf = None
                    ajo_rect = None
                except Exception:
                    pass
                # cambiar la imagen de Drácula si tenemos variante resguardada
                if dracula_resguardado_img is not None:
                    dracula_img = dracula_resguardado_img
                else:
                    # intentar atenuar la imagen original para dar efecto "resguardado"
                    try:
                        alt = dracula_img.copy()
                        alt.fill((120,120,120,0), special_flags=pygame.BLEND_RGBA_MULT)
                        dracula_img = alt
                    except Exception:
                        pass

        # --- ACTUALIZAR ESTADO DE DRÁCULA RESGUARDADO ---
        if dracula_resguardado_activo:
            dracula_resguardado_timer -= dt
            if dracula_resguardado_timer <= 0:
                # "desaparece"
                dracula_resguardado_activo = False
                dracula_visible = False
                try:
                    hitbox_dracula.size = (0, 0)
                except Exception:
                    pass
                limite_activo = False
                mostrar_hitboxes = False

        try:
            btn_config.draw(screen)
        except Exception:
            pass

        inv.update(dt)
        inv.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    iniciar_sala4(crear_inventario())
