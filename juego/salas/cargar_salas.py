import pygame, sys

from juego.controlador.cargar_fondos import cargar_fondo
from juego.limite_colisiones.colision_piso import colision_piso, devolver_puntos_hexagono
from juego.controlador.sprites_caminar import sprites_caminar
from juego.controlador.controles import teclas_movimiento
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from juego.controlador.cargar_config import get_config_sala
from juego.controlador.boton_config import crear_boton_config, abrir_menu_config
from juego.controlador.boton_config import crear_boton_config, abrir_menu_config

# Añadido: Item para guardar el papel en el inventario
from juego.ui.inventory import Item

def cargar_sala(nombre_sala, maniquies=[], inv=None, objetos_sala=[]):
    """Carga una sala con un fondo dado.
    Más adelante podés expandirla con enemigos, puertas, etc."""

    general = get_config_sala("general")
    size = tamaño_pantallas()
    screen = info_pantalla()
    fuente = general["fuente"]
    config = get_config_sala(nombre_sala)

    pos_inicial = config["personaje"]["pos_inicial"],
    tamaño = config["personaje"]["tamaño"]

    fondo = cargar_fondo(config["fondo"], "Fondos")
    personaje, personaje_rect = general["personaje"], general["personaje_rect"]

    # Botón de configuración (es creado por sala para que funcione en todas las salas)
    btn_config = crear_boton_config(size[0] - 140, 20)

    # Puerta
    puerta_interaccion_salida = config["puertas"]["salida"]
    try:
        puerta_interaccion_volver = config["puertas"]["volver"]
    except KeyError:
        puerta_interaccion_volver = None

    puntos_hexagono = devolver_puntos_hexagono()
    mask = colision_piso(size)

    mostrar_contorno = False
    inv = inv
    
    # Variables para el mensaje de error
    mensaje_error_timer = 0
    mensaje_error_duracion = 2  # duración en segundos
    mensaje_error_activo = False
    mensaje_error_texto = ""
    # Variables para interacción/recogida de objetos
    interaccion_texto = ""
    interaccion_timer = 0.0
    interaccion_target = None

    # -------------------------------------------------------

    clock = pygame.time.Clock()
    velocidad = 2
    print(f"[DEBUG] sala config cargada: siguiente={config.get('siguiente_sala')}, puertas={config.get('puertas')}")
    while True:
        dt = clock.tick(35) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # manejador del botón de configuración
            try:
                btn_config.handle_event(event, lambda: abrir_menu_config(screen))
            except Exception:
                pass

            # Llamada al manejador del inventario con protección para evitar crash
            try:
                inv.handle_event(event)
            except Exception as e:
                import traceback
                print("ERROR en inv.handle_event:")
                traceback.print_exc()
                continue

        if not inv.is_open:
            # Actualizar posición del personaje según teclas antes de comprobar interacciones
            # DEBUG: imprimir posición antes
            # print(f"DEBUG antes movimiento: {personaje_rect.topleft}")
            moving, direction = teclas_movimiento(personaje_rect, velocidad, inv, mask, maniquies)
            # DEBUG: imprimir posición despues si hubo movimiento
            if moving:
                print(f"DEBUG movimiento: new topleft={personaje_rect.topleft} moving={moving} direction={direction}")
            # Recalcular pies del personaje con la nueva posición
            # Aumentamos el área de detección de los pies para facilitar la interacción
            pies_personaje = pygame.Rect(
                personaje_rect.centerx - 20,
                personaje_rect.bottom - 10,
                40, 10
            )
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif teclas[pygame.K_F1]:
                mostrar_contorno = not mostrar_contorno

            # Detectar objeto cercano para mostrar prompt (rango reducido a 25px)
            interaccion_target = None
            DIST_THRESHOLD = 25  # rango en pixeles para mostrar prompt
            for objeto in objetos_sala:
                if objeto.get('rect') is None:
                    # rect no creado: ignorar
                    continue
                collided = pies_personaje.colliderect(objeto['rect'])
                obj_center = objeto['rect'].center
                player_point = (personaje_rect.centerx, personaje_rect.bottom)
                dx = obj_center[0] - player_point[0]
                dy = obj_center[1] - player_point[1]
                dist = (dx*dx + dy*dy) ** 0.5
                close_enough = dist <= DIST_THRESHOLD
                if objeto.get('visible') and (collided or close_enough):
                    interaccion_target = objeto
                    break

            # Si se pulsa E, intentar recoger el objeto (si hay uno) o interactuar con puertas
            if teclas[pygame.K_e]:
                if interaccion_target:
                    from juego.controlador.agregar_inv import agregar_a_inventario
                    added = agregar_a_inventario(interaccion_target, inv)
                    if added:
                        interaccion_texto = f"Recogiste {interaccion_target.get('nombre')}"
                        interaccion_timer = 1.5
                    else:
                        interaccion_texto = f"No se pudo recoger {interaccion_target.get('nombre')}"
                        interaccion_timer = 1.5

                # Interacción puerta salida (E)
                if puerta_interaccion_salida and pies_personaje.colliderect(puerta_interaccion_salida):
                    missing = any(obj.get('visible', True) for obj in objetos_sala)
                    if missing:
                        mensaje_error_activo = True
                        mensaje_error_timer = mensaje_error_duracion
                        mensaje_error_texto = "se necesitan todos los objetos antes de pasar de sala"
                    else:
                        siguiente = config.get('siguiente_sala')
                        if siguiente:
                            return siguiente

                # Interacción puerta volver (E)
                if puerta_interaccion_volver and pies_personaje.colliderect(puerta_interaccion_volver):
                    print(f"[DEBUG] volver a sala anterior: {config.get('sala_anterior')}")
                    return config["sala_anterior"]

            # Si hay un objeto cercano y no se ha pulsado E, mostrar el prompt
            if interaccion_target and not teclas[pygame.K_e]:
                # Mostrar prompt mientras el jugador esté en el rango
                interaccion_texto = f"Presiona E para recoger {interaccion_target.get('nombre')}"
            else:
                # Si el jugador se aleja y no hay mensaje de recogida en curso, limpiar prompt
                if interaccion_timer <= 0:
                    interaccion_texto = ""
                
        # Empty list for maniquies since this room has none
        maniquies = maniquies if maniquies else []

        try:
            inv.update(dt)
        except Exception:
            import traceback
            print("ERROR en inv.update:")
            traceback.print_exc()

        # Crear superficie para el overlay de texto
        overlay = pygame.Surface(size, pygame.SRCALPHA)
        mensaje_mostrado = False

        # Dibujar fondo primero
        screen.blit(fondo, (0, 0))

        # Dibujar objetos del suelo
        for objeto in objetos_sala:
            try:
                if objeto.get('visible') and objeto.get('surf_suelo') and objeto.get('rect'):
                    screen.blit(objeto['surf_suelo'], objeto['rect'].topleft)
            except Exception as e:
                print(f"ERROR dibujando objeto {objeto.get('nombre')}: {e}")

        # Mostrar contornos de debug si corresponde
        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)
            pygame.draw.rect(screen, (0, 0, 255), personaje_rect, 1)
            pygame.draw.rect(screen, (0, 255, 255), pies_personaje, 2)
            pygame.draw.rect(screen, (255, 0, 0), puerta_interaccion_salida, 2)
            if puerta_interaccion_volver:
                pygame.draw.rect(screen, (255, 0, 0), puerta_interaccion_volver, 2)

        # Renderizar sprites (animación) después del fondo para que no sean sobreescritos
        # sprites_caminar ahora devuelve la superficie del jugador para permitir ordenar
        # por profundidad con otros objetos. Aquí la usamos y la añadimos a la lista
        # de objetos a dibujar (esta sala no tiene maniquíes normalmente).
        current_player_surf = sprites_caminar(size, screen, inv, mask, maniquies, tamaño, personaje, personaje_rect)
        objetos = ([(m["img"], m["rect"]) for m in maniquies] if maniquies else []) + [(current_player_surf, personaje_rect)]
        objetos.sort(key=lambda x: x[1].bottom)
        for img, rect in objetos:
            screen.blit(img, rect)

        # Mostrar texto de interacción/recogida si aplica
        if interaccion_texto:
            try:
                texto_inter = fuente.render(interaccion_texto, True, (255, 255, 255))
                screen.blit(texto_inter, (size[0] // 2 - texto_inter.get_width() // 2, size[1] - 70))
            except Exception:
                pass
        # decrementar timer si se usó uno (mensaje de recogida)
        if interaccion_timer > 0:
            interaccion_timer -= dt
            if interaccion_timer <= 0:
                interaccion_texto = ""
                interaccion_timer = 0.0
        # Mensajes de interacción con puertas
        if pies_personaje.colliderect(puerta_interaccion_salida):
            texto = fuente.render("Presiona E para pasar a la siguiente sala", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))
        # Si durante el bucle se construyó un overlay con mensajes, blitearlo encima
        if mensaje_mostrado:
            try:
                screen.blit(overlay, (0, 0))
            except Exception:
                # En caso de que algo vaya mal con el overlay, no romper el loop
                pass

        inv.draw(screen)

        # dibujar botón de configuración encima de la escena
        try:
            btn_config.draw(screen)
        except Exception:
            pass

        try:
            inv.draw(screen)
        except Exception:
            import traceback
            print("ERROR en inv.draw:")
            traceback.print_exc()
        # Mostrar mensaje de error si está activo
        if mensaje_error_activo:
            mensaje_error_timer -= dt
            texto_error = fuente.render(mensaje_error_texto, True, (255, 100, 100))
            screen.blit(texto_error, (size[0] // 2 - texto_error.get_width() // 2, size[1] - 140))
            if mensaje_error_timer <= 0:
                mensaje_error_activo = False

        pygame.display.flip()
        continue

        #return info_personaje, fuente, inv, pies_personaje, teclas, puerta_interaccion_salida