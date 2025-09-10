import pygame, sys

from juego.controlador.cargar_fondos import cargar_fondo

def pantalla_de_inicio():
    pygame.init()
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escape del Juicio")

    bg = cargar_fondo("pantallainicial.png", "Fondos", (WIDTH, HEIGHT))
    font = pygame.font.SysFont("arial", 48, bold=True)
    fuente_agresiva = pygame.font.SysFont("impact", 60)
    color_rojo = (255, 0, 0)

    class Button:
        def __init__(self, rect, text, callback):
            self.rect = pygame.Rect(rect)
            self.text = text
            self.callback = callback
            self.hover = False

        def draw(self, surface):
            base_color = (120, 0, 0)
            hover_color = (180, 0, 0)
            border_color = (200, 200, 200)
            color = hover_color if self.hover else base_color
            pygame.draw.rect(surface, color, self.rect, border_radius=12)
            pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=12)
            # Usa fuente agresiva y color rojo para el texto del botón
            text_surf = fuente_agresiva.render(self.text, True, color_rojo)
            text_rect = text_surf.get_rect(center=self.rect.center)
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
        for b in buttons:
            b.draw(screen)

        pygame.display.flip()
        clock.tick(60)
