import pygame, sys, os

# Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from juego.salas.cargar_salas import cargar_sala
from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_config import get_config_sala
from juego.controlador.inventario import crear_inventario
from juego.controlador.cargar_personaje import cargar_personaje
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

    # Cargar el hacha
    hacha_img, hacha_rect = cargar_personaje("hacha_piso.png", "objetos", size, tamaño=(60, 80))
    hacha_rect.topleft = (900, 350)  # Posición del hacha (ligeramente detrás de donde estará Drácula)

    # Cargar a Drácula
    dracula_img, dracula_rect = cargar_personaje("dracula.png", "dracula", size, tamaño=(180, 200))
    dracula_rect.topleft = (700, 340)  # Posición de Drácula en la sala

    # Área de interacción con Drácula
    hitbox_dracula = pygame.Rect(
        dracula_rect.left + 20,
        dracula_rect.bottom - 30,
        dracula_rect.width - 40,
        30
    )

    personaje, personaje_rect = general["personaje"], general["personaje_rect"]
    fuente = general["fuente"]

    # Variables de estado
    mostrar_hitboxes = True
    mensaje_texto = ""
    mensaje_color = (255, 255, 255)
    mensaje_timer = 0

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

        # Dibujar hacha, personaje y Drácula según profundidad
        objetos = [(hacha_img, hacha_rect), (dracula_img, dracula_rect), (current_player_surf, personaje_rect)]
        objetos.sort(key=lambda x: x[1].bottom)
        for img, rect in objetos:
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

        # Verificar colisiones con la puerta
        pies_personaje = pygame.Rect(personaje_rect.centerx - 10, personaje_rect.bottom - 5, 20, 5)
        if pies_personaje.colliderect(config["puertas"]["salida"]):
            mensaje_texto = "Presiona E para pasar a la siguiente sala"
            if teclas[pygame.K_e]:
                return "siguiente_sala"

        # Verificar interacción con Drácula
        if personaje_rect.colliderect(hitbox_dracula):
            mensaje_texto = "¡Has encontrado a Drácula!"

        if mensaje_timer > 0:
            mensaje_timer -= dt
        else:
            mensaje_color = (255, 255, 255)

        # Mostrar hitboxes en modo debug
        if mostrar_hitboxes:
            pygame.draw.rect(screen, (255, 0, 0), hitbox_dracula, 1)

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