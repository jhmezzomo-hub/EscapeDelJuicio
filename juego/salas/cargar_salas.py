import pygame, sys, os

from juego.controlador.cargar_fondos import cargar_fondo
from juego.limite_colisiones.colision_piso import colision_piso, devolver_puntos_hexagono
from juego.controlador.sprites_caminar import sprites_caminar
from juego.controlador.controles import teclas_movimiento
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from juego.controlador.inventario import crear_inventario
from juego.controlador.cargar_config import get_config_sala
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
            moving, direction = teclas_movimiento(personaje_rect, velocidad, inv, mask, maniquies)
            # Recalcular pies del personaje con la nueva posición
            pies_personaje = pygame.Rect(
                personaje_rect.centerx - 10,
                personaje_rect.bottom - 5,
                20, 5
            )
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif teclas[pygame.K_F1]:
                mostrar_contorno = not mostrar_contorno
            elif teclas[pygame.K_e]:
                # Comprobar interacción con objetos
                for objeto in objetos_sala:
                    if objeto['visible'] and pies_personaje.colliderect(objeto['rect']):
                        from juego.controlador.agregar_inv import agregar_a_inventario
                        agregar_a_inventario(objeto, inv)
                
                # Interacción: puerta salida / volver
                if puerta_interaccion_salida:
                    if pies_personaje.colliderect(puerta_interaccion_salida):
                        print(f"[DEBUG] paso a siguiente sala: {config.get('siguiente_sala')}")
                        return config["siguiente_sala"]
                if puerta_interaccion_volver:
                    if pies_personaje.colliderect(puerta_interaccion_volver) and puerta_interaccion_volver:
                        print(f"[DEBUG] volver a sala anterior: {config.get('sala_anterior')}")
                        return config["sala_anterior"]
                
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
        
        # Dibujar objetos de la sala
        for objeto in objetos_sala:
            if objeto['visible']:
                if objeto['surf_suelo'] and objeto['rect']:
                    screen.blit(objeto['surf_suelo'], objeto['rect'])
                    if pies_personaje.colliderect(objeto['rect']):
                        mensaje = f"Presiona E para recoger {objeto['nombre']}"
                        texto = fuente.render(mensaje, True, (255, 255, 255))
                        y_pos = size[1] - 70 if objeto['nombre'] == "papel" else size[1] - 100
                        # Agregar fondo semi-transparente al texto
                        texto_rect = texto.get_rect(center=(size[0] // 2, y_pos))
                        padding = 10
                        fondo_texto = pygame.Surface((texto_rect.width + padding*2, texto_rect.height + padding*2), pygame.SRCALPHA)
                        fondo_texto.fill((0, 0, 0, 128))  # Negro semi-transparente
                        overlay.blit(fondo_texto, (texto_rect.centerx - fondo_texto.get_width()//2, texto_rect.y - padding))
                        overlay.blit(texto, texto_rect)
                        mensaje_mostrado = True

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

        # Mensajes de interacción con puertas
        if pies_personaje.colliderect(puerta_interaccion_salida):
            texto = fuente.render("Presiona E para pasar a la siguiente sala", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))
        elif puerta_interaccion_volver and pies_personaje.colliderect(puerta_interaccion_volver):
            texto = fuente.render("Presiona E para volver a la sala anterior", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))
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
        pygame.display.flip()
        continue

        #return info_personaje, fuente, inv, pies_personaje, teclas, puerta_interaccion_salida