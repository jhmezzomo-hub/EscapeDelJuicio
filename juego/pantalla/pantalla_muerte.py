import pygame, sys, os
import pygame.freetype
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from info_pantalla.info_pantalla import info_pantalla, tamaño_pantallas
from juego.pantalla.pantalla_inicio import pantalla_de_inicio

def pantalla_fin():
    size = tamaño_pantallas()
    screen = info_pantalla()

    bg = cargar_fondo("game_over.png", "Fondos")
    if bg is None:
        try:
            bg = pygame.image.load(os.path.join("Fondos", "game_over.png"))
            bg = pygame.transform.scale(bg, size)
        except Exception:
            bg = pygame.Surface(size)
            bg.fill((10, 10, 10))

    try:
        fuente_agresiva = pygame.freetype.SysFont("impact", 48, bold=True)
    except Exception:
        fuente_agresiva = pygame.freetype.SysFont(None, 48, bold=True)

    color_texto_normal = (110, 10, 10)
    color_texto_hover = (170, 20, 20)
    outline_color = (0, 0, 0)
    outline_size = 3

    def render_texto(texto, color, center):
        rect_medida = fuente_agresiva.get_rect(texto)
        w = rect_medida.width + outline_size * 2 + 6
        h = rect_medida.height + outline_size * 2 + 6

        text_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        text_surf.fill((0, 0, 0, 0))

        for ox in range(-outline_size, outline_size + 1):
            for oy in range(-outline_size, outline_size + 1):
                if ox == 0 and oy == 0:
                    continue
                fuente_agresiva.render_to(text_surf, (outline_size + ox, outline_size + oy),
                                         texto, fgcolor=outline_color, bgcolor=None)

        fuente_agresiva.render_to(text_surf, (outline_size, outline_size),
                                 texto, fgcolor=color, bgcolor=None)

        text_rect = text_surf.get_rect(center=center)
        return text_surf, text_rect

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
            self.mask = pygame.mask.from_surface(self.text_surf)
            surface.blit(self.text_surf, self.text_rect)

        def handle_event(self, event):
            if self.text_rect is None or self.mask is None:
                return
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                mouse_pos = event.pos
                if self.text_rect.collidepoint(mouse_pos):
                    local_x = mouse_pos[0] - self.text_rect.x
                    local_y = mouse_pos[1] - self.text_rect.y
                    if 0 <= local_x < self.text_surf.get_width() and 0 <= local_y < self.text_surf.get_height():
                        if self.mask.get_at((int(local_x), int(local_y))):
                            self.hover = True
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                if callable(self.callback):
                                    self.callback()
                            return
                self.hover = False

    running = True
    result = None
    def start_game():
        nonlocal running
        nonlocal result
        result = 'replay'
        running = False

    def exit_game():
        pygame.quit()
        sys.exit()

    def go_menu():
        # Cerrar esta pantalla y abrir el menú principal.
        nonlocal running, result
        result = 'menu'
        running = False

    btn_w, btn_h = 300, 70
    gap = btn_h + 20
    x = int(size[0] * 0.75)
    y0 = int(size[1] * 0.50)

    btn_play = Button((x - btn_w//2, y0, btn_w, btn_h), "VOLVER A JUGAR", start_game)
    btn_menu = Button((x - btn_w//2, y0 + gap, btn_w, btn_h), "VOLVER AL MENU", go_menu)
    btn_exit = Button((x - btn_w//2, y0 + 2*gap, btn_w, btn_h), "SALIR", exit_game)
    buttons = [btn_play, btn_menu, btn_exit]

    clock = pygame.time.Clock()
    while running:
        screen.blit(bg, (0, 0))
        for b in buttons:
            b.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for b in buttons:
                b.handle_event(event)
        pygame.display.flip()
        clock.tick(60)
    return result