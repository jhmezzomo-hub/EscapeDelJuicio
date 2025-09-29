import pygame, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
size = tamaño_pantallas()
screen = info_pantalla()

# Colores
NEGRO = (0, 0, 0)
ROJO_OSCURO = (139, 0, 0)
ROJO_SANGRE = (180, 0, 0)
DORADO = (212, 165, 116)
BLANCO = (255, 255, 255)

# Fuentes
fuente_titulo = pygame.font.Font(None, 120)
fuente_subtitulo = pygame.font.Font(None, 50)
fuente_botones = pygame.font.Font(None, 60)

class Boton:
    def __init__(self, x, y, ancho, alto, texto, accion):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.accion = accion
        self.hover = False
        self.color_normal = ROJO_OSCURO
        self.color_hover = ROJO_SANGRE
        
    def dibujar(self, superficie):
        # Color del botón según si está en hover
        color = self.color_hover if self.hover else self.color_normal
        
        # Sombra del botón
        sombra = self.rect.copy()
        sombra.x += 5
        sombra.y += 5
        pygame.draw.rect(superficie, (0, 0, 0), sombra, border_radius=10)
        
        # Botón principal
        pygame.draw.rect(superficie, color, self.rect, border_radius=10)
        pygame.draw.rect(superficie, DORADO, self.rect, 3, border_radius=10)
        
        # Efecto de brillo si está en hover
        if self.hover:
            brillo = self.rect.copy()
            brillo.inflate_ip(-10, -10)
            pygame.draw.rect(superficie, (200, 0, 0, 50), brillo, border_radius=8)
        
        # Texto del botón
        texto_surface = fuente_botones.render(self.texto, True, DORADO)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        superficie.blit(texto_surface, texto_rect)
    
    def verificar_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)
    
    def verificar_click(self, pos):
        if self.rect.collidepoint(pos):
            return self.accion
        return None

def pantalla_muerte():
    reloj = pygame.time.Clock()
    
    # Crear botones
    botones = [
        Boton(size[0]//2 - 200, size[1]//2 + 50, 400, 80, "VOLVER A JUGAR", "reiniciar"),
        Boton(size[0]//2 - 200, size[1]//2 + 150, 400, 80, "MENÚ PRINCIPAL", "menu"),
        Boton(size[0]//2 - 200, size[1]//2 + 250, 400, 80, "SALIR", "salir")
    ]
    
    # Variables para efectos
    alpha_fondo = 0
    fade_in = True
    tiempo_glitch = 0
    
    # Cargar imagen de fondo (opcional)
    # fondo = pygame.image.load("ruta_a_tu_imagen.png")
    # fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    
    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        pos_mouse = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEMOTION:
                for boton in botones:
                    boton.verificar_hover(pos_mouse)
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    accion = boton.verificar_click(pos_mouse)
                    if accion == "reiniciar":
                        print("Reiniciando juego...")
                        return "reiniciar"
                    elif accion == "menu":
                        print("Volviendo al menú...")
                        return "menu"
                    elif accion == "salir":
                        pygame.quit()
                        sys.exit()
        
        # Fondo degradado oscuro
        for y in range(size[1]):
            color = (int(26 * (1 - y/size[1])), 0, 0)
            pygame.draw.line(screen, color, (0, y), (size[0], y))
        
        # Aquí puedes dibujar tu imagen de fondo
        # pantalla.blit(fondo, (0, 0))
        # Aplicar oscurecimiento
        overlay = pygame.Surface(size)
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Efecto de fade in
        if fade_in and alpha_fondo < 255:
            alpha_fondo += 3
            if alpha_fondo >= 255:
                fade_in = False
        
        # Título "GAME OVER" con efecto glitch
        tiempo_glitch += 1
        offset_x = 0
        offset_y = 0
        if tiempo_glitch % 30 < 5:  # Efecto glitch ocasional
            offset_x = pygame.math.Vector2(2, -2)[tiempo_glitch % 2]
            offset_y = pygame.math.Vector2(-2, 2)[tiempo_glitch % 2]
        
        # Sombra del título
        texto_titulo = fuente_titulo.render("GAME OVER", True, (0, 0, 0))
        rect_titulo = texto_titulo.get_rect(center=(size[0]//2 + 5, size[1]//4 + 5))
        screen.blit(texto_titulo, rect_titulo)
        
        # Título principal
        texto_titulo = fuente_titulo.render("GAME OVER", True, ROJO_OSCURO)
        rect_titulo = texto_titulo.get_rect(center=(size[0]//2 + offset_x, size[1]//4 + offset_y))
        screen.blit(texto_titulo, rect_titulo)
        
        # Subtítulo
        texto_sub = fuente_subtitulo.render("EL JUICIO TE HA ATRAPADO", True, DORADO)
        rect_sub = texto_sub.get_rect(center=(size[0]//2, size[1]//4 + 80))
        screen.blit(texto_sub, rect_sub)
        
        # Dibujar botones
        for boton in botones:
            boton.dibujar(screen)
        
        pygame.display.flip()
    
    return None

pantalla_muerte()
"""# Ejecutar la pantalla de muerte
if __name__ == "__main__":
    resultado = pantalla_muerte()
    print(f"Acción seleccionada: {resultado}")
    pygame.quit()"""