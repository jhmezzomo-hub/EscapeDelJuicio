import pygame.freetype, sys
from juego.pantalla.tutorial import tutorial

from juego.controlador.cargar_fondos import cargar_fondo
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla

def pantalla_de_inicio():
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

    # Resto del código igual, solo cambia render_texto

    class Button:
        def __init__(self, rect, text, callback):
            self.rect = pygame.Rect(rect)
            self.text = text
            self.callback = callback
            self.hover = False
            self.text_surf = None
            self.text_rect = None
            self.mask = None

        def draw(self, surface):
            text_color = color_texto_hover if self.hover else color_texto_normal
            self.text_surf, self.text_rect = render_texto(self.text, text_color, self.rect.center)
            # Crear máscara para detección precisa
            if not self.mask:
                self.mask = pygame.mask.from_surface(self.text_surf)
            surface.blit(self.text_surf, self.text_rect)

        def handle_event(self, event):
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                mouse_pos = event.pos
                if self.text_rect and self.text_rect.collidepoint(mouse_pos):
                    # Convertir posición global del mouse a local de la superficie de texto
                    local_x = mouse_pos[0] - self.text_rect.x
                    local_y = mouse_pos[1] - self.text_rect.y
                    # Verificar si el punto está dentro de la máscara
                    if 0 <= local_x < self.text_surf.get_width() and 0 <= local_y < self.text_surf.get_height():
                        if self.mask.get_at((local_x, local_y)):
                            self.hover = True
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                self.callback()
                            return
                self.hover = False

    running = True
    def start_game():
        nonlocal running
        running = False

    def tuto():
        # Abrir la pantalla de tutorial y volver al menú al cerrarla
        tutorial()

    def exit_game():
        pygame.quit()
        sys.exit()

    btn_w, btn_h = 250, 70
    btn_play = Button((850, int(size[1]*0.65)-20, btn_w, btn_h), "JUGAR", start_game)
    btn_tuto = Button((850, int(size[1]*0.65)+45, btn_w, btn_h), "TUTORIAL", tuto)
    btn_exit = Button((850, int(size[1]*0.65)+110, btn_w, btn_h), "SALIR", exit_game)
    buttons = [btn_play, btn_tuto, btn_exit]

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            for b in buttons:
                b.handle_event(event)

        screen.blit(bg, (0, 0))

        for b in buttons:
            b.draw(screen)

        pygame.display.flip()
        clock.tick(60)
