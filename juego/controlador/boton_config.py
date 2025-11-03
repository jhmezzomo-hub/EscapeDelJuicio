import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.pantalla.pantalla_inicio import pantalla_de_inicio

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
    def __init__(self, rect, text=None, font=None, bg=(50, 50, 50), fg=(255,255,255)):
        if isinstance(rect, (tuple, list)):
            self.rect = pygame.Rect(rect)
        else:
            self.rect = rect
        self.text = str(text) if text else None
        self.font = font or pygame.font.SysFont(None, 24)
        self.bg = bg
        self.fg = fg
        # Cargar la imagen del botón
        image_path = os.path.join(os.path.dirname(__file__), '..', '..', 'img', 'logos', 'boton-config.png')
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (75,75))

    def draw(self, surface):
        # Dibujar la imagen del botón
        surface.blit(self.image, self.rect)

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
    opciones = ["Volver al menú"]
    seleccion = 0

    # (overlay eliminado) usamos sólo el panel semitransparente

    # Configuración del menú
    menu_w, menu_h = 400, 300
    # Calculamos el centro exacto de la pantalla
    menu_x = (ancho-menu_w) // 2
    menu_y = (alto-menu_h) // 2  # Desplazamiento hacia arriba para mejor equilibrio visual
    
    # Configuración de la barra de volumen
    barra_ancho = 200
    barra_alto = 20
    barra_x = menu_x + (menu_w - barra_ancho) // 2
    barra_y = menu_y + 100
    barra_rect = pygame.Rect(barra_x, barra_y, barra_ancho, barra_alto)
    
    # Slider (control deslizante)
    slider_ancho = 20
    slider_alto = 30
    slider_y = barra_y - (slider_alto - barra_alto) // 2
    
    dragging = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    mouse_pos = event.pos
                    
                    if barra_rect.collidepoint(mouse_pos) or pygame.Rect(barra_x, barra_y - slider_alto//2, barra_ancho, slider_alto).collidepoint(mouse_pos):
                        dragging = True
                        # Actualizar volumen basado en la posición del click
                        nuevo_x = max(barra_x, min(mouse_pos[0], barra_x + barra_ancho))
                        volumen = (nuevo_x - barra_x) / barra_ancho
                        aplicar_volumen()
                    
                    # Verificar clicks en los botones
                    boton_y = menu_y + menu_h - 100
                    boton_ancho = (menu_w - 60) // 2
                    
                    # Comprobar click en "Volver al menú"
                    menu_rect = pygame.Rect(menu_x + 20, boton_y, boton_ancho, 40)
                    if menu_rect.collidepoint(mouse_pos):
                        # Guardar el estado actual
                        old_screen = screen.copy()
                        # Mostrar pantalla de inicio
                        pantalla_de_inicio()
                        # Restaurar el estado anterior
                        screen.blit(old_screen, (0,0))
                        pygame.display.flip()
                        running = False
                    
                    # Comprobar click en "Volver al juego"
                    juego_rect = pygame.Rect(menu_x + 20 + boton_ancho + 20, boton_y, boton_ancho, 40)
                    if juego_rect.collidepoint(mouse_pos):
                        running = False
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    # Actualizar volumen mientras se arrastra
                    nuevo_x = max(barra_x, min(event.pos[0], barra_x + barra_ancho))
                    volumen = (nuevo_x - barra_x) / barra_ancho
                    aplicar_volumen()

    # Dibujado del menú (sin overlay; el panel es semitransparente)

        # Panel (usar superficie con canal alfa para permitir transparencia)
        panel = pygame.Surface((menu_w, menu_h), pygame.SRCALPHA)
        # Relleno semitransparente (RGBA) — ajusta el último valor (0-255) para más/menos transparencia
        panel.fill((30, 30, 30, 180))
        # Borde opaco
        pygame.draw.rect(panel, (200,200,200), panel.get_rect(), 2)
        print(f"[DEBUG] Dibujando panel en ({menu_x},{menu_y}) tamaño ({menu_w}x{menu_h})")
        
        # Añadir un margen superior
        margen_superior = 30

        # Título
        titulo = title_font.render("Configuración", True, (255,255,255))
        panel.blit(titulo, ((menu_w - titulo.get_width())//2, margen_superior))

        # Barra de volumen
        # Texto "Volumen"
        vol_label = fuente.render("Volumen", True, (255, 255, 255))
        menu_barra_x = (menu_w - barra_ancho) // 2
        menu_barra_y = 100
        panel.blit(vol_label, ((menu_w - vol_label.get_width()) // 2, menu_barra_y - 40))

        # Porcentaje de volumen
        vol_percent = fuente.render(f"{int(volumen * 100)}%", True, (255, 255, 255))
        panel.blit(vol_percent, ((menu_w - vol_percent.get_width()) // 2, menu_barra_y - 20))

        # Actualizar las coordenadas absolutas de la barra para la detección de clicks
        barra_x = menu_x + menu_barra_x
        barra_y = menu_y + menu_barra_y
        barra_rect = pygame.Rect(barra_x, barra_y, barra_ancho, barra_alto)

        # Dibujar la barra en el panel usando coordenadas relativas al panel
        panel_barra_rect = pygame.Rect(menu_barra_x, menu_barra_y, barra_ancho, barra_alto)
        pygame.draw.rect(panel, (100, 100, 100), panel_barra_rect)  # Barra base
        # Dibujar la parte llena de la barra
        volumen_rect = pygame.Rect(menu_barra_x, menu_barra_y, barra_ancho * volumen, barra_alto)
        pygame.draw.rect(panel, (0, 255, 0), volumen_rect)  # Barra de progreso
        pygame.draw.rect(panel, (255, 255, 255), panel_barra_rect, 2)  # Borde

        # Slider (se dibuja en coordenadas relativas al panel)
        slider_x = barra_x + (barra_ancho * volumen) - (slider_ancho // 2)
        slider_y = barra_y - (slider_alto - barra_alto) // 2
        # Convertir a coordenadas relativas al panel antes de dibujar
        slider_rect = pygame.Rect(slider_x - menu_x, slider_y - menu_y, slider_ancho, slider_alto)
        pygame.draw.rect(panel, (200, 200, 200), slider_rect)
        pygame.draw.rect(panel, (100, 100, 100), slider_rect, 2)

        # Botones en la parte inferior
        boton_y = menu_h - 100  # Subimos los botones
        boton_ancho = (menu_w - 60) // 2  # Ancho para cada botón (20 de margen a los lados, 20 entre botones)
        boton_alto = 40

        # Botón Volver al menú (izquierda)
        menu_rect = pygame.Rect(menu_w//4 - boton_ancho//2, boton_y, boton_ancho, boton_alto)
        pygame.draw.rect(panel, (50, 50, 50), menu_rect)
        pygame.draw.rect(panel, (200, 200, 200), menu_rect, 2)
        menu_text = fuente.render("Volver al menú", True, (255, 255, 255))
        boton_menu_x = menu_rect.x + (menu_rect.width - menu_text.get_width()) // 2
        boton_menu_y = menu_rect.y + (menu_rect.height - menu_text.get_height()) // 2
        # Usar coordenadas locales del panel (boton_menu_x, boton_menu_y)
        panel.blit(menu_text, (boton_menu_x, boton_menu_y))

        # Botón Volver al juego (derecha)
        juego_rect = pygame.Rect(3*menu_w//4 - boton_ancho//2, boton_y, boton_ancho, boton_alto)
        pygame.draw.rect(panel, (50, 50, 50), juego_rect)
        pygame.draw.rect(panel, (200, 200, 200), juego_rect, 2)
        juego_text = fuente.render("Volver al juego", True, (255, 255, 255))
        juego_x = juego_rect.x + (juego_rect.width - juego_text.get_width()) // 2
        juego_y = juego_rect.y + (juego_rect.height - juego_text.get_height()) // 2
        panel.blit(juego_text, (juego_x, juego_y))

        # Blit del panel en la pantalla
        screen.blit(panel, (menu_x, menu_y))

        pygame.display.flip()
        clock.tick(60)


def crear_boton_config(x, y, size=60, text="Config"):
    font = pygame.font.SysFont(None, 24)
    return Button((x, y, size, size), text, font=font)


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
