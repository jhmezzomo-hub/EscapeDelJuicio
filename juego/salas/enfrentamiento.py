import pygame.freetype, sys
from juego.pantalla.tutorial import tutorial

from juego.controlador.cargar_fondos import cargar_fondo
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla

def pantalla_de_enfrentamiento():
    size = tamaño_pantallas()
    screen = info_pantalla()

    bg = cargar_fondo("pantallainicial.png", "Fondos")

    # Usamos freetype para fuente con contorno
    fuente_agresiva = pygame.freetype.SysFont("impact", 72, bold=True)

    color_texto_normal = (110, 10, 10)   # rojo sangre oscura
    color_texto_hover = (170, 20, 20)    # más brillante al pasar el mouse
    outline_color = (0, 0, 0)            # negro para contorno
    outline_size = 3                     # grosor del contorno

    def render_texto(texto, color, center):
        # Creamos superficie transparente para el texto
        text_surf = pygame.Surface((500, 150), pygame.SRCALPHA)
        text_surf.fill((0,0,0,0))

        # Crear el efecto de contorno dibujando el texto en varias posiciones
        offsets = [(x, y) for x in [-outline_size, 0, outline_size] for y in [-outline_size, 0, outline_size]]
        for offset_x, offset_y in offsets:
            if offset_x != 0 or offset_y != 0:  # Skip center position for outline
                fuente_agresiva.render_to(text_surf, (outline_size + offset_x, outline_size + offset_y), texto, fgcolor=outline_color, bgcolor=None)

        # Dibujamos el texto principal en el centro
        fuente_agresiva.render_to(text_surf, (outline_size, outline_size), texto, fgcolor=color, bgcolor=None)

        text_rect = text_surf.get_rect(center=center)
        return text_surf, text_rect