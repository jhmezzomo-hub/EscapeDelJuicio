import pygame, sys, os

# Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_config import get_config_sala
from juego.controlador.inventario import crear_inventario
from juego.controlador.sprites_caminar import sprites_caminar
from juego.limite_colisiones.colision_piso import colision_piso
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from juego.controlador.boton_config import crear_boton_config, abrir_menu_config

# Importar las otras salas
from juego.salas.sala3 import iniciar_sala3
from juego.salas.sala7 import iniciar_sala7


def iniciar_sala6(inv):
    if inv is None:
        inv = crear_inventario()

    size = tamaño_pantallas()
    screen = info_pantalla()
    general = get_config_sala("general")
    config = get_config_sala("sala6")

    personaje, personaje_rect = general["personaje"], general["personaje_rect"]
    personaje_rect.topleft = config["personaje"]["pos_inicial"]
    fuente = general["fuente"]

    # === Fondo y colisiones ===
    fondo = cargar_fondo("fondo_sala6.png", "Fondos")
    mask = colision_piso(size)

    # === Cargar imagen de la nave (grande) ===
    ruta_img = os.path.join(project_root, "img", "nave", "nave.png")
    nave_img = pygame.image.load(ruta_img).convert_alpha()
    nave_img = pygame.transform.scale(nave_img, (400, 300))
    nave_rect = nave_img.get_rect(center=(size[0] // 2, size[1] // 2 + 50))

    # === HITBOX PERSONALIZADA DE LA NAVE ===
    hitbox_nave = pygame.Rect(
        nave_rect.centerx - 100,
        nave_rect.centery + 100,  # bajada 60 px
        200,
        60
    )

    nave_obj = {
        "img": nave_img,
        "rect": nave_rect,
        "hitbox": hitbox_nave,
        "profundidad": (nave_rect.top, nave_rect.bottom)
    }

    btn_config = crear_boton_config(size[0] - 140, 20)
    clock = pygame.time.Clock()

    mensaje_texto = ""
    mensaje_color = (255, 255, 255)
    mostrar_hitbox = False

    while True:
        dt = clock.tick(60) / 1000.0
        teclas = pygame.key.get_pressed()
        screen.blit(fondo, (0, 0))

        # === Zonas de interacción ===
        zona_retorno = pygame.Rect(size[0] // 2 - 70, size[1] - 60, 140, 60)
        # Subimos 20 píxeles respecto a la versión anterior
        zona_interaccion_nave = pygame.Rect(
            nave_rect.centerx - 80,
            nave_rect.bottom - 30,  # antes -10
            160,
            70
        )

        objetos_en_sala = [nave_obj]
        current_player_surf = sprites_caminar(size, screen, inv, mask, objetos_en_sala,
                                            personaje_rect.size, personaje, personaje_rect)

        lista_para_dibujar = [(nave_obj["img"], nave_obj["rect"]), (current_player_surf, personaje_rect)]
        lista_para_dibujar.sort(key=lambda x: x[1].bottom)
        for img, rect in lista_para_dibujar:
            screen.blit(img, rect)

        hitbox_pies = pygame.Rect(personaje_rect.centerx - 10, personaje_rect.bottom - 8, 20, 8)

        en_zona_retorno = hitbox_pies.colliderect(zona_retorno)
        en_zona_nave = hitbox_pies.colliderect(zona_interaccion_nave)

        if en_zona_nave:
            mensaje_texto = "Presione E para subirse a la nave"
            if teclas[pygame.K_e]:
                iniciar_sala7()
                return
        elif en_zona_retorno:
            mensaje_texto = "Presione E para volver a la sala anterior"
            if teclas[pygame.K_e]:
                iniciar_sala3(inv)
                return
        else:
            mensaje_texto = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                mostrar_hitbox = not mostrar_hitbox

            btn_config.handle_event(event, lambda: abrir_menu_config(screen))
            inv.handle_event(event)

        if mostrar_hitbox:
            pygame.draw.rect(screen, (255, 0, 0), hitbox_nave, 2)
            pygame.draw.rect(screen, (0, 255, 0), zona_interaccion_nave, 2)
            pygame.draw.rect(screen, (0, 0, 255), zona_retorno, 2)
            pygame.draw.rect(screen, (255, 255, 0), hitbox_pies, 2)

        if mensaje_texto:
            texto = fuente.render(mensaje_texto, True, mensaje_color)
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 60))

        btn_config.draw(screen)
        inv.update(dt)
        inv.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    iniciar_sala6(crear_inventario())
