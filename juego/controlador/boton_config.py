import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

"""Botón de configuración y menú modal.

Provee:
- Button: clase ligera para dibujar y detectar clicks
- crear_boton_config(x,y,w,h,text): helper para crear el botón
- abrir_menu_config(screen): abre un menú modal con opciones:
  "Subir Volumen", "Bajar Volumen", "Volver al menú"

Nota: la opción de volumen actualiza una variable de módulo `volumen` y
intenta aplicar `pygame.mixer.music.set_volume(volumen)` si el mixer está
inicializado (si no, sólo actualiza el valor en memoria).
"""

volumen = 0.5  # valor entre 0.0 y 1.0


class Button:
    def __init__(self, rect, text, font=None, bg=(50, 50, 50), fg=(255,255,255)):
        self.rect = pygame.Rect(rect)
        self.text = str(text)
        self.font = font or pygame.font.SysFont(None, 24)
        self.bg = bg
        self.fg = fg

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg, self.rect)
        pygame.draw.rect(surface, (0,0,0), self.rect, 2)
        txt = self.font.render(self.text, True, self.fg)
        tx = self.rect.x + (self.rect.width - txt.get_width()) // 2
        ty = self.rect.y + (self.rect.height - txt.get_height()) // 2
        surface.blit(txt, (tx, ty))

    def is_hover(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event, on_click=None):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hover(event.pos):
                if on_click:
                    on_click()
                return True
        return False


def aplicar_volumen():
    """Intenta aplicar el volumen al mixer si está inicializado."""
    global volumen
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(volumen)
    except Exception:
        # No hacemos nada si falla; el valor se conserva en la variable
        pass


def abrir_menu_config(screen):
    """Abre un menú modal de configuración.

    Parámetros:
    - screen: superficie donde dibujar el menú (se usa modalmente)

    El menú gestiona su propio loop hasta que el usuario selecciona
    "Volver al menú" o cierra la ventana.
    """
    global volumen
    clock = pygame.time.Clock()
    ancho, alto = screen.get_size()
    fuente = pygame.font.SysFont(None, 28)
    title_font = pygame.font.SysFont(None, 34)

    # Opciones del menú
    opciones = ["Subir Volumen", "Bajar Volumen", "Volver al menú"]
    seleccion = 0

    # Overlay semitransparente
    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((0,0,0,150))

    def subir():
        global volumen
        volumen = min(1.0, round((volumen + 0.1), 2))
        aplicar_volumen()

    def bajar():
        global volumen
        volumen = max(0.0, round((volumen - 0.1), 2))
        aplicar_volumen()

    actions = [subir, bajar, lambda: None]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if opciones[seleccion] == "Volver al menú":
                        running = False
                    else:
                        actions[seleccion]()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # detectar clicks en las opciones
                mx, my = event.pos
                menu_w, menu_h = 400, 260
                menu_x = (ancho - menu_w) // 2
                menu_y = (alto - menu_h) // 2
                # cada opción tiene altura
                opt_h = 60
                for i, _ in enumerate(opciones):
                    rect = pygame.Rect(menu_x + 20, menu_y + 60 + i * opt_h, menu_w - 40, opt_h - 10)
                    if rect.collidepoint((mx, my)):
                        if opciones[i] == "Volver al menú":
                            running = False
                        else:
                            actions[i]()

        # Dibujado del menú
        screen.blit(overlay, (0, 0))
        menu_w, menu_h = 400, 260
        menu_x = (ancho - menu_w) // 2
        menu_y = (alto - menu_h) // 2

        # Panel
        panel = pygame.Surface((menu_w, menu_h))
        panel.fill((30, 30, 30))
        pygame.draw.rect(panel, (200,200,200), panel.get_rect(), 2)

        # Título
        titulo = title_font.render("Configuración", True, (255,255,255))
        panel.blit(titulo, ((menu_w - titulo.get_width())//2, 10))

        # Mostrar volumen actual
        vol_txt = fuente.render(f"Volumen: {int(volumen*100)}%", True, (200,200,150))
        panel.blit(vol_txt, ((menu_w - vol_txt.get_width())//2, 45))

        # Opciones
        opt_h = 60
        for i, opt in enumerate(opciones):
            rect = pygame.Rect(20, 60 + i * opt_h, menu_w - 40, opt_h - 10)
            color = (70,70,70) if i != seleccion else (100,100,140)
            pygame.draw.rect(panel, color, rect)
            txt = fuente.render(opt, True, (255,255,255))
            panel.blit(txt, (rect.x + 10, rect.y + (rect.height - txt.get_height())//2))

        # Blit panel
        screen.blit(panel, (menu_x, menu_y))

        pygame.display.flip()
        clock.tick(60)


def crear_boton_config(x, y, w=120, h=40, text="Config"):
    font = pygame.font.SysFont(None, 24)
    return Button((x, y, w, h), text, font=font)


if __name__ == "__main__":
    # pequeño demo si se ejecuta el módulo directamente
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    btn = crear_boton_config(20, 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if btn.handle_event(event, lambda: abrir_menu_config(screen)):
                pass

        screen.fill((80, 80, 80))
        btn.draw(screen)
        pygame.display.flip()
