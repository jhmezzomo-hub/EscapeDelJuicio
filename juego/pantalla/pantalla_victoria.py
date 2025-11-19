import pygame, sys, os
import pygame.freetype
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from info_pantalla.info_pantalla import info_pantalla, tamaño_pantallas
from juego.pantalla.pantalla_inicio import pantalla_de_inicio

def pantalla_victoria():
    size = tamaño_pantallas()
    screen = info_pantalla()

    bg = cargar_fondo("victoria.png", "Fondos")
    if bg is None:
        try:
            bg = pygame.image.load(os.path.join("Fondos", "victoria.png"))
            bg = pygame.transform.scale(bg, size)
        except Exception:
            bg = pygame.Surface(size)
            bg.fill((10, 10, 10))

    try:
        fuente_agresiva = pygame.freetype.SysFont("impact", 48, bold=True)
    except Exception:
        fuente_agresiva = pygame.freetype.SysFont(None, 48, bold=True)

    color_texto_normal = (0, 204, 255)
    color_texto_hover = (0, 134, 166)
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

    def exit_game():
        pygame.quit()
        sys.exit()

    def go_menu():
        # Cerrar esta pantalla y abrir el menú principal.
        nonlocal running, result
        result = 'menu'
        running = False

    # Configuración de botones horizontales
    btn_w, btn_h = 200, 70  # Botones más pequeños para que quepan horizontalmente
    gap_horizontal = 100     # Más espacio entre botones horizontalmente
    total_width = 2 * btn_w + gap_horizontal  # Ancho total que ocuparán los 2 botones
    x_start = size[0] // 4  # Más hacia la izquierda (25% del ancho en lugar de centrado)
    y = int(size[1] * 0.70)  # Posición vertical (más abajo para dar espacio al texto)

    # Crear botones uno al lado del otro
    btn_menu = Button((x_start, y, btn_w, btn_h), "VOLVER AL MENU", go_menu)
    btn_exit = Button((x_start + btn_w + gap_horizontal, y, btn_w, btn_h), "SALIR", exit_game)
    buttons = [btn_menu, btn_exit]

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