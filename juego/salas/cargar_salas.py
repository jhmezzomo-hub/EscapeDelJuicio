import pygame, sys, os

from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_personaje import cargar_personaje
from limite_colisiones.colision_piso import colision_piso, devolver_puntos_hexagono
from juego.controlador.sprites_caminar import sprites_caminar
from juego.controlador.controles import teclas_movimiento
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from juego.controlador.inventario import crear_inventario
from juego.controlador.cargar_config import get_config_sala

# Añadido: Item para guardar el papel en el inventario
from juego.ui.inventory import Item

def cargar_sala(nombre_sala, maniquies=[]):
    """Carga una sala con un fondo dado.
    Más adelante podés expandirla con enemigos, puertas, etc."""

    size = tamaño_pantallas()
    screen = info_pantalla()
    fuente = pygame.font.SysFont("Arial", 26)
    config = get_config_sala(nombre_sala)

    pos_inicial = config["personaje"]["pos_inicial"],
    tamaño = config["personaje"]["tamaño"]

    fondo = cargar_fondo(config["fondo"], "Fondos")
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", size, tamaño)

    # Puerta
    puerta_interaccion_salida = config["puertas"]["salida"]
    try:
        puerta_interaccion_volver = config["puertas"]["volver"]
    except KeyError:
        puerta_interaccion_volver = None

    #pies_personjae
    pies_personaje = pygame.Rect(
            personaje_rect.centerx - 10,
            personaje_rect.bottom - 5,
            20, 5
        )

    puntos_hexagono = devolver_puntos_hexagono()
    mask = colision_piso(size)

    mostrar_contorno = False
    inv = crear_inventario()

    # --- Nuevo: crear un papel en sala "inicio" (sala 1) ---
    papel_visible = False
    papel_surf = None
    papel_rect = None
    papel_inv_surf = None  # Nueva superficie para la imagen en el inventario
    
    # --- Agregar variables para la linterna ---
    linterna_visible = False
    linterna_surf = None
    linterna_rect = None
    linterna_inv_surf = None
    
    if nombre_sala in ("inicio", "sala1", "sala_1"):
        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'img', 'objetos'))
        try:
            # Cargar las imágenes usando los nombres exactos de los archivos
            papel_inv_surf = pygame.image.load(os.path.join(img_dir, "papel_inv.png")).convert_alpha()
            papel_surf = pygame.image.load(os.path.join(img_dir, "papel_piso.png")).convert_alpha()
            # Para la linterna, usar la misma imagen
            linterna_surf = pygame.image.load(os.path.join(img_dir, "linterna.png")).convert_alpha()
            linterna_inv_surf = linterna_surf  # Usar la misma imagen
            
            print(f"Imágenes cargadas exitosamente desde: {img_dir}")  # Para debug
            
        except Exception as e:
            print(f"Error al cargar imágenes: {e}")  # Para debug
            papel_surf = None
            papel_inv_surf = None
            linterna_surf = None
            linterna_inv_surf = None

        # Tamaños diferentes para suelo e inventario
        papel_size = (40, 30)  # tamaño en suelo
        papel_inv_size = (32, 32)  # tamaño en inventario

        # Crear/escalar imagen del suelo
        if papel_surf is None:
            papel_surf = pygame.Surface(papel_size, pygame.SRCALPHA)
            papel_surf.fill((245, 245, 220))
            pygame.draw.rect(papel_surf, (200, 200, 180), papel_surf.get_rect(), 1)
        else:
            try:
                papel_surf = pygame.transform.smoothscale(papel_surf, papel_size)
            except Exception:
                papel_surf = pygame.transform.scale(papel_surf, papel_size)

        # Crear/escalar imagen del inventario
        if papel_inv_surf is None:
            papel_inv_surf = papel_surf.copy()  # usar la misma que en suelo si no hay específica
        else:
            try:
                papel_inv_surf = pygame.transform.smoothscale(papel_inv_surf, papel_inv_size)
            except Exception:
                papel_inv_surf = pygame.transform.scale(papel_inv_surf, papel_inv_size)

        papel_rect = papel_surf.get_rect(topleft=(200, 500))
        papel_visible = True

        # Configurar linterna
        linterna_size = (40, 30)  # tamaño en suelo
        linterna_inv_size = (32, 32)  # tamaño en inventario

        # Crear/escalar imagen de linterna en suelo
        if linterna_surf is None:
            linterna_surf = pygame.Surface(linterna_size, pygame.SRCALPHA)
            linterna_surf.fill((200, 200, 100))  # Color amarillento para la linterna
            pygame.draw.rect(linterna_surf, (150, 150, 50), linterna_surf.get_rect(), 1)
        else:
            try:
                linterna_surf = pygame.transform.smoothscale(linterna_surf, linterna_size)
            except Exception:
                linterna_surf = pygame.transform.scale(linterna_surf, linterna_size)

        # Crear/escalar imagen de linterna en inventario
        if linterna_inv_surf is None:
            linterna_inv_surf = linterna_surf.copy()
        else:
            try:
                linterna_inv_surf = pygame.transform.smoothscale(linterna_inv_surf, linterna_inv_size)
            except Exception:
                linterna_inv_surf = pygame.transform.scale(linterna_inv_surf, linterna_inv_size)

        linterna_rect = linterna_surf.get_rect(topleft=(600, 500))  # Posición opuesta al papel
        linterna_visible = True

    # -------------------------------------------------------

    clock = pygame.time.Clock()
    velocidad = 5
    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            inv.handle_event(event)

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
                # Interacción: puerta salida / volver
                if puerta_interaccion_salida:
                    if pies_personaje.colliderect(puerta_interaccion_salida):
                        return config["siguiente_sala"]
                if puerta_interaccion_volver:
                    if pies_personaje.colliderect(puerta_interaccion_volver) and puerta_interaccion_volver:
                        return config["sala_anterior"]
                # Interacción: recoger papel si está visible y el jugador está encima
                if papel_visible and papel_rect and pies_personaje.colliderect(papel_rect):
                    # meter el papel en la primera ranura libre del inventario
                    try:
                        # la estructura del inventario espera inventory_slots (o similar)
                        # intentamos colocar en inv.inventory_slots si existe
                        placed = False
                        if hasattr(inv, "inventory_slots"):
                            for i in range(len(inv.inventory_slots)):
                                if inv.inventory_slots[i] is None:
                                    # Usar papel_inv_surf en lugar de papel_surf
                                    inv.inventory_slots[i] = Item(type="objetos", count=1, max_stack=1, 
                                                               color=(255,255,255), image=papel_inv_surf)
                                    placed = True
                                    break
                        # si tiene método add_item (otra implementación), intentar usarlo
                        if not placed and hasattr(inv, "add_item"):
                            # crear Item compatible con add_item (puede esperar otro tipo),
                            # aquí asumimos que add_item quiere objetos con item_id/name; hacemos fallback mínimo
                            try:
                                inv.add_item(Item)  # no falla la llamada en la mayoría de implementaciones; si falla, lo atrapamos
                            except Exception:
                                pass
                        # si no se pudo colocar, dejar el papel en el suelo (no quitar)
                        if placed:
                            papel_visible = False
                    except Exception:
                        # en caso de error no romper el bucle; solo no recoger
                        papel_visible = papel_visible
                # Interacción: recoger linterna
                if linterna_visible and linterna_rect and pies_personaje.colliderect(linterna_rect):
                    try:
                        placed = False
                        if hasattr(inv, "inventory_slots"):
                            for i in range(len(inv.inventory_slots)):
                                if inv.inventory_slots[i] is None:
                                    inv.inventory_slots[i] = Item(type="linterna", count=1, max_stack=1, 
                                                               color=(255,255,0), image=linterna_inv_surf)
                                    placed = True
                                    break
                        if placed:
                            linterna_visible = False
                    except Exception:
                        linterna_visible = linterna_visible

        # Empty list for maniquies since this room has none
        maniquies = maniquies if maniquies else []

        inv.update(dt)

        # Dibujar fondo primero
        screen.blit(fondo, (0, 0))

        # Mostrar contornos de debug si corresponde
        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)
            pygame.draw.rect(screen, (0, 0, 255), personaje_rect, 1)
            pygame.draw.rect(screen, (0, 255, 255), pies_personaje, 2)
            pygame.draw.rect(screen, (255, 0, 0), puerta_interaccion_salida, 2)
            if puerta_interaccion_volver:
                pygame.draw.rect(screen, (255, 0, 0), puerta_interaccion_volver, 2)

        # Dibujar el papel en el piso si está visible
        if papel_visible and papel_surf and papel_rect:
            screen.blit(papel_surf, papel_rect)

        # Dibujar la linterna en el suelo si está visible
        if linterna_visible and linterna_surf and linterna_rect:
            screen.blit(linterna_surf, linterna_rect)

        # Renderizar sprites (animación) después del fondo para que no sean sobreescritos
        sprites_caminar(size, screen, inv, mask, maniquies, tamaño, personaje, personaje_rect)

        # Mensajes de interacción con puertas
        if pies_personaje.colliderect(puerta_interaccion_salida):
            texto = fuente.render("Presiona E para pasar a la siguiente sala", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))
        elif puerta_interaccion_volver and pies_personaje.colliderect(puerta_interaccion_volver):
            texto = fuente.render("Presiona E para volver a la sala anterior", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))
        # Mensaje para recoger papel
        if papel_visible and papel_rect and pies_personaje.colliderect(papel_rect):
            texto = fuente.render("Presiona E para recoger el papel", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 70))
        # Mensaje para recoger linterna
        if linterna_visible and linterna_rect and pies_personaje.colliderect(linterna_rect):
            texto = fuente.render("Presiona E para recoger la linterna", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 100))

        inv.draw(screen)
        pygame.display.flip()
