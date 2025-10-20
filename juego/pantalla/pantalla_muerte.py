import pygame, sys, os
import pygame.freetype

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.pantalla.pantalla_inicio import pantalla_de_inicio
from juego.controlador.cargar_fondos import cargar_fondo
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla

def pantalla_fin():
    pygame.init()
    # (opcional) pygame.freetype.init()  # no suele ser necesario porque pygame.init() ya lo hace

    size = tamaño_pantallas()          # espera (width, height)
    screen = info_pantalla()           # superficie pygame.Surface

    # Cargar fondo (asegurate que cargar_fondos devuelva una Surface escalada o una Surface normal)
    bg = cargar_fondo("game_over.png", "Fondos", size)
    if bg is None:
        # fallback: intenta cargar directamente
        try:
            bg = pygame.image.load(os.path.join("Fondos", "game_over.png"))
            bg = pygame.transform.scale(bg, size)
        except Exception:
            bg = pygame.Surface(size)
            bg.fill((10, 10, 10))

    # Fuente freetype (con contorno)
    try:
        fuente_agresiva = pygame.freetype.SysFont("impact", 48, bold=True)
    except Exception:
        fuente_agresiva = pygame.freetype.SysFont(None, 48, bold=True)

    color_texto_normal = (110, 10, 10)   # rojo oscuro
    color_texto_hover = (170, 20, 20)    # rojo más brillante
    outline_color = (0, 0, 0)
    outline_size = 3

    def render_texto(texto, color, center):
        # medir texto para crear superficie exacta
        rect_medida = fuente_agresiva.get_rect(texto)
        w = rect_medida.width + outline_size * 2 + 6
        h = rect_medida.height + outline_size * 2 + 6

        text_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        text_surf.fill((0, 0, 0, 0))

        # dibujar contorno con offsets
        for ox in range(-outline_size, outline_size + 1):
            for oy in range(-outline_size, outline_size + 1):
                if ox == 0 and oy == 0:
                    continue
                fuente_agresiva.render_to(text_surf, (outline_size + ox, outline_size + oy),
                                         texto, fgcolor=outline_color, bgcolor=None)

        # dibujar texto principal
        fuente_agresiva.render_to(text_surf, (outline_size, outline_size),
                                 texto, fgcolor=color, bgcolor=None)

        text_rect = text_surf.get_rect(center=center)
        return text_surf, text_rect

    class Button:
        def __init__(self, rect, text, callback):
            self.rect = pygame.Rect(rect)    # rect usado sólo para posicionamiento
            self.text = text
            self.callback = callback         # referencia a la función (NO ejecutada aquí)
            self.hover = False
            self.text_surf = None
            self.text_rect = None
            self.mask = None

        def draw(self, surface):
            text_color = color_texto_hover if self.hover else color_texto_normal
            self.text_surf, self.text_rect = render_texto(self.text, text_color, self.rect.center)
            # (Re)crear máscara cada draw para estar seguro si la superficie cambia
            self.mask = pygame.mask.from_surface(self.text_surf)
            surface.blit(self.text_surf, self.text_rect)

        def handle_event(self, event):
            # sólo proceder si ya hay rect y máscara creados
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
                                # ejecutar callback (referencia)
                                if callable(self.callback):
                                    self.callback()
                            return
                self.hover = False

    running = True
    def start_game():
        nonlocal running
        running = False     # salimos del loop para "reiniciar"

    def exit_game():
        pygame.quit()
        sys.exit()

    # Posiciones en columna, alineados a la derecha
    btn_w, btn_h = 300, 70
    gap = btn_h + 20  # separación entre botones

    # anclamos en el 80% del ancho (parte derecha)
    x = int(size[0] * 0.75)
    y0 = int(size[1] * 0.50)  # arrancan un poco más arriba del centro

    btn_play = Button((x - btn_w//2, y0, btn_w, btn_h), "VOLVER A JUGAR", start_game)
    btn_menu = Button((x - btn_w//2, y0 + gap, btn_w, btn_h), "VOLVER AL MENU", pantalla_de_inicio)
    btn_exit = Button((x - btn_w//2, y0 + 2*gap, btn_w, btn_h), "SALIR", exit_game)
    buttons = [btn_play, btn_menu, btn_exit]


    clock = pygame.time.Clock()

    # Dibujo primero para que las máscaras existan antes de procesar eventos
    while running:
        # dibujar fondo y botones (crea text_rect y mask)
        screen.blit(bg, (0, 0))
        for b in buttons:
            b.draw(screen)

        # eventos (ahora que hay máscaras)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for b in buttons:
                b.handle_event(event)

        pygame.display.flip()
        clock.tick(60)

pantalla_fin()