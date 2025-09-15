import pygame, sys
from juego.controlador.cargar_fondos import cargar_fondo

def pantalla_de_inicio():
    pygame.init()
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escape del Juicio")

    bg = cargar_fondo("pantallainicial.png", "Fondos", (WIDTH, HEIGHT))
    fuente_agresiva = pygame.font.SysFont("impact", 72, bold=True)

    # Colores más oscuros
    color_texto_normal = (110, 10, 10)   # rojo sangre oscura
    color_texto_hover = (170, 20, 20)    # más brillante al pasar el mouse
    color_borde_exterior = (0, 0, 0)     # negro
    color_borde_interior = (0, 0, 0)     # borde interno, más suave

    def render_texto(texto, color, center):
        # Renderizamos texto principal
        text_surf = fuente_agresiva.render(texto, True, color)
        text_rect = text_surf.get_rect()

        # Superficie para contorno
        outline = pygame.Surface((text_rect.width + 20, text_rect.height + 20), pygame.SRCALPHA)

        # Borde exterior grueso
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx != 0 or dy != 0:
                    outline.blit(fuente_agresiva.render(texto, True, color_borde_exterior), (dx + 10, dy + 10))

        # Borde interior sutil
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            outline.blit(fuente_agresiva.render(texto, True, color_borde_interior), (dx + 10, dy + 10))

        # Texto final encima
        outline.blit(text_surf, (10, 10))

        return outline, outline.get_rect(center=center)

    class Button:
        def __init__(self, rect, text, callback):
            self.rect = pygame.Rect(rect)
            self.text = text
            self.callback = callback
            self.hover = False

        def draw(self, surface):
            text_color = color_texto_hover if self.hover else color_texto_normal
            text_surf, text_rect = render_texto(self.text, text_color, self.rect.center)
            surface.blit(text_surf, text_rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEMOTION:
                self.hover = self.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.callback()

    running = True
    def start_game():
        nonlocal running
        running = False

    def exit_game():
        pygame.quit()
        sys.exit()

    btn_w, btn_h = 250, 70
    btn_play = Button((700, int(HEIGHT*0.65), btn_w, btn_h), "JUGAR", start_game)
    btn_exit = Button((700, int(HEIGHT*0.65)+90, btn_w, btn_h), "SALIR", exit_game)
    buttons = [btn_play, btn_exit]

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            for b in buttons:
                b.handle_event(event)

        screen.blit(bg, (0, 0))

        # Botones
        for b in buttons:
            b.draw(screen)

        pygame.display.flip()
        clock.tick(60)
