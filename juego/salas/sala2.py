import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from juego.limite_colisiones.colision_piso import colision_piso
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import manejar_mc
from info_pantalla.info_pantalla import info_pantalla, tamaño_pantallas 
from juego.pantalla.ensombrecer import ensombrecer
from juego.ui.inventory import Inventory

def iniciar_sala2():
    pygame.init()
    size = tamaño_pantallas()
    screen = info_pantalla()

    fuente = pygame.font.SysFont("Arial", 26)
    fondo = cargar_fondo("Fondo_sala1.png", "Fondos", size)
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", size)
    velocidad = 5

    #Crear puerta de regreso a sala 1
    puerta_regreso = pygame.Rect(550 - 80, 550, 180, 180)

    mask = colision_piso(size)

    maniquies = []
    posiciones = [
        (850, 250), (910, 400), (730, 340),
        (20, 400), (150, 250), (250, 340)
    ]
    imagenes = ["mm1.png", "mm2.png", "mm3.png", "mm4.png", "mm5.png", "mm6.png"]
    tamaños = [
        (180, 180), (184, 190), (110, 200),
        (110, 200), (110, 200), (186, 200)
    ]

    for img, pos, (ancho, alto) in zip(imagenes, posiciones, tamaños):
        maniquie_img, maniquie_rect = cargar_personaje(img, "Michael Myers", size)
        maniquie_img = pygame.transform.scale(maniquie_img, (ancho, alto))
        maniquie_rect = maniquie_img.get_rect()
        maniquie_rect.topleft = pos

        # Crear hitbox personalizada
        hitbox_rect = pygame.Rect(maniquie_rect.left + 20, maniquie_rect.top + 50,
                                   maniquie_rect.width - 40, maniquie_rect.height - 50)

        maniquies.append((maniquie_img, maniquie_rect, hitbox_rect))

    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            inv.handle_event(event)

        if not inv.is_open:
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif teclas[pygame.K_F1]:
                mostrar_contorno = not mostrar_contorno
            elif teclas[pygame.K_e]:
                pies_personaje = pygame.Rect(
                    personaje_rect.centerx - 10,
                    personaje_rect.bottom - 5,
                    20, 5
                )
                if pies_personaje.colliderect(puerta_regreso):
                    # Regresar a la sala anterior
                    return "sala1"

        manejar_mc(personaje_rect, inv, mask, velocidad, maniquies)

        # Primero dibujamos el fondo
        screen.blit(fondo, (0, 0))

        # Luego verificamos la colisión con la puerta
        pies_personaje = pygame.Rect(
            personaje_rect.centerx - 10,
            personaje_rect.bottom - 5,
            20, 5
        )

        # Ordenar objetos por profundidad
        objetos = [(img, rect) for img, rect, _ in maniquies] + [(personaje, personaje_rect)]
        objetos.sort(key=lambda x: x[1].bottom)

        for img, rect in objetos:
            screen.blit(img, rect)
            if rect != personaje_rect:
                hitbox_index = [m[1] for m in maniquies].index(rect)
                hitbox_rect = maniquies[hitbox_index][2]
                pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 1)  # Opcional: dibuja la hitbox

                if personaje_rect.colliderect(hitbox_rect):
                    texto = fuente.render("¡Colisión con maniquí!", True, (255, 0, 0))
                    screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        # Verificar si el personaje está en la puerta y mostrar mensaje
        if pies_personaje.colliderect(puerta_regreso):
            texto = fuente.render("Presiona E para regresar a la sala anterior", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        inv.update(dt)

        inv.draw(screen)
        ensombrecer(screen)
        pygame.display.flip()

if __name__ == "__main__":
    iniciar_sala2()
