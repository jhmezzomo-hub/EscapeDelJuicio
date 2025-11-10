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

def iniciar_sala4(inv):
    if inv is None:
        inv = crear_inventario()
        
    size = tamaño_pantallas()
    screen = info_pantalla()
    general = get_config_sala("general")
    config = get_config_sala("sala4")

    # Cargar el hacha usando cargar_objeto para incluir imagen de inventario
    objeto_hacha = cargar_objeto("hacha", (900, 350), (60, 80), (40, 40))
    objetos_sala = [objeto_hacha]

    # Cargar a Drácula
    dracula_img, dracula_rect = cargar_personaje("dracula.png", "dracula", size, tamaño=(180, 200))
    dracula_rect.topleft = (700, 340)  # Posición de Drácula en la sala

    # Línea límite a la izquierda de Drácula en el piso
    limite_x = dracula_rect.left - 10

    # Área de interacción con Drácula
    hitbox_dracula = pygame.Rect(
        dracula_rect.left + 20,
        dracula_rect.bottom - 30,
        dracula_rect.width - 40,
        30
    )

    personaje, personaje_rect = general["personaje"], general["personaje_rect"]
    personaje_rect.topleft = config["personaje"]["pos_inicial"]
    fuente = general["fuente"]

    # Variables de estado
    mostrar_hitboxes = True
    mensaje_texto = ""
    mensaje_color = (255, 255, 255)
    mensaje_timer = 0

    # Nueva: duración de los mensajes y flags para detectar entrada en zonas
    mensaje_duracion = 1  # segundos que debe mostrarse el mensaje
    prev_en_puerta = False
    prev_en_dracula = False

    # Máscara para colisiones
    mask = colision_piso(size)

    # Cargar fondo
    fondo = cargar_fondo("Fondo_sala1.png", "Fondos")

    # Botón de configuración
    btn_config = crear_boton_config(size[0] - 140, 20)

    clock = pygame.time.Clock()

    # Lista para colisiones (necesaria para sprites_caminar)
    obstaculos = [{"hitbox": hitbox_dracula}]

    while True:
        dt = clock.tick(60) / 1000.0
        teclas = pygame.key.get_pressed()

        # Dibujar fondo
        screen.blit(fondo, (0, 0))

        # Actualizar movimiento y animación del personaje
        current_player_surf = sprites_caminar(size, screen, inv, mask, obstaculos, personaje_rect.size, personaje, personaje_rect)

        # Dibujar objetos de sala visibles (incluye hacha), Drácula y personaje según profundidad
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

        # Definir pies del personaje (se usa para varias comprobaciones)
        pies_personaje = pygame.Rect(personaje_rect.centerx - 10, personaje_rect.bottom - 5, 20, 5)
        
        # Overlay para mensajes contextuales (transparente)
        overlay = pygame.Surface(size, pygame.SRCALPHA)
        mensaje_mostrado = False

        # Mostrar prompts para objetos de sala y manejar recogida con E (misma lógica que cargar_salas)
        for objeto in objetos_sala:
            if objeto.get("visible") and objeto.get("surf_suelo") and objeto.get("rect"):
                # si el jugador está cerca, mostrar prompt
                if pies_personaje.colliderect(objeto["rect"]):
                    mensaje = f"Presiona E para recoger {objeto.get('nombre', 'objeto')}"
                    texto = fuente.render(mensaje, True, (255, 255, 255))
                    y_pos = size[1] - 70 if objeto.get("nombre") == "papel" else size[1] - 100
                    texto_rect = texto.get_rect(center=(size[0] // 2, y_pos))
                    padding = 10
                    fondo_texto = pygame.Surface((texto_rect.width + padding*2, texto_rect.height + padding*2), pygame.SRCALPHA)
                    fondo_texto.fill((0, 0, 0, 128))
                    overlay.blit(fondo_texto, (texto_rect.x - padding, texto_rect.y - padding))
                    overlay.blit(texto, texto_rect)
                    mensaje_mostrado = True
                    # Si pulsa E, intentar agregar al inventario y ocultar el objeto
                    if teclas[pygame.K_e]:
                        try:
                            from juego.controlador.agregar_inv import agregar_a_inventario
                            try:
                                # Llamada directa como en cargar_salas: agregar_a_inventario(objeto, inv)
                                agregar_a_inventario(objeto, inv)
                            except Exception:
                                # fallback sencillo: intentar forma inversa
                                try:
                                    agregar_a_inventario(inv, objeto)
                                except Exception:
                                    # si falla, no interrumpir el juego
                                    pass
                        except Exception:
                            pass
                        objeto["visible"] = False

        # Dibujar overlay encima
        screen.blit(overlay, (0, 0))

        # Verificar colisiones con la puerta (usar pies_personaje ya calculado)
        en_puerta = pies_personaje.colliderect(config["puertas"]["salida"])
        # Mostrar el mensaje sólo cuando se entra en la zona (no continuamente)
        if en_puerta and not prev_en_puerta:
            mensaje_texto = "Presiona E para pasar a la siguiente sala"
            mensaje_timer = mensaje_duracion
        # Permitir pasar aunque el mensaje ya haya expirado
        if en_puerta and teclas[pygame.K_e]:
            return "siguiente_sala"
        prev_en_puerta = en_puerta

        # Verificar si el personaje cruza el límite (a la izquierda de Drácula)
        if personaje_rect.left > limite_x:
            return "muerte"  # Terminar el juego si cruza el límite

        # Verificar interacción con Drácula (mostrar mensaje sólo al entrar)
        en_dracula = personaje_rect.colliderect(hitbox_dracula)
        if en_dracula and not prev_en_dracula:
            mensaje_texto = "¡Has encontrado a Drácula!"
            mensaje_timer = mensaje_duracion
        prev_en_dracula = en_dracula

        # Actualizar temporizador del mensaje y ocultarlo cuando expire
        if mensaje_timer > 0:
            mensaje_timer -= dt
            if mensaje_timer <= 0:
                mensaje_texto = ""
        else:
            mensaje_color = (255, 255, 255)

        # Mostrar hitboxes en modo debug
        if mostrar_hitboxes:
            pygame.draw.rect(screen, (255, 0, 0), hitbox_dracula, 1)
            # Dibujar línea límite roja inclinada a la izquierda de Drácula, como dibujada en el piso
            pygame.draw.line(screen, (255, 0, 0), (limite_x, dracula_rect.bottom), (limite_x - 100, size[1]), 2)

        # Renderizar mensajes
        if mensaje_texto:
            texto = fuente.render(mensaje_texto, True, mensaje_color)
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        # Dibujar elementos de UI
        try:
            btn_config.draw(screen)
        except Exception:
            pass

        inv.update(dt)
        inv.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    # Al ejecutar directamente, pasar un inventario creado para evitar errores
    iniciar_sala4(crear_inventario())