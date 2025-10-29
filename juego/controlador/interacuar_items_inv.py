import pygame

class ItemViewer:
    def __init__(self):
        self.viewing_item = None
        self.view_background = None
        self.font = pygame.font.SysFont("Arial", 24)

    def show_item(self, item):
        """Activa la vista ampliada para un item."""
        if item and hasattr(item, 'image') and item.image:
            # Crear fondo semitransparente una vez
            if not self.view_background:
                bg = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
                bg.fill((0, 0, 0, 180))
                self.view_background = bg
            self.viewing_item = item
            return True
        return False

    def handle_event(self, event):
        """Maneja eventos para cerrar la vista ampliada."""
        if self.viewing_item and event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            self.viewing_item = None
            return True
        return False

    def draw(self, surface):
        """Dibuja la vista ampliada del item si está activa."""
        if not self.viewing_item or not self.view_background:
            return

        # Dibujar fondo semitransparente
        surface.blit(self.view_background, (0, 0))
        
        # Obtener dimensiones
        screen_width, screen_height = surface.get_size()
        
        # Calcular tamaño (70% de la altura)
        view_height = int(screen_height * 0.7)
        img = self.viewing_item.image
        img_ratio = img.get_width() / img.get_height()
        view_width = int(view_height * img_ratio)
        
        try:
            scaled_img = pygame.transform.smoothscale(img, (view_width, view_height))
        except:
            scaled_img = pygame.transform.scale(img, (view_width, view_height))
        
        # Centrar en pantalla
        img_rect = scaled_img.get_rect(center=(screen_width//2, screen_height//2))
        surface.blit(scaled_img, img_rect)
        
        # Texto de ayuda
        hint = self.font.render("Click o ESC para cerrar", True, (255, 255, 255))
        hint_rect = hint.get_rect(bottom=screen_height-20, centerx=screen_width//2)
        surface.blit(hint, hint_rect)

def mostrar_item_ampliado(screen, item):
    """Función de ayuda para mostrar un item ampliado sin crear una instancia."""
    viewer = ItemViewer()
    if viewer.show_item(item):
        viewer.draw(screen)
        pygame.display.flip()
        # Esperar hasta que el usuario cierre
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if viewer.handle_event(event):
                    waiting = False
                    break