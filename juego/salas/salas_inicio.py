import sys, os, pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.inventario import crear_inventario

class SalaInicio:
    def __init__(self, ventana):
        self.ventana = ventana
        self.inventario = crear_inventario(ventana)
        self.fuente = pygame.font.SysFont("Arial", 26)

    def actualizar(self, personaje_rect, rect_puerta):
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.inventario.click(pos)

        # Verificar uso de llave en puerta
        teclas = pygame.key.get_pressed()
        if personaje_rect.colliderect(rect_puerta):
            if self.inventario.tiene_objeto("Llave"):
                if teclas[pygame.K_e]:  # Presionar E para usar la llave
                    self.inventario.usar("Llave")
                    return "siguiente_sala"
            else:
                texto = self.fuente.render("Necesitas una llave", True, (255, 255, 255))
                self.ventana.blit(texto, (self.ventana.get_width()//2 - texto.get_width()//2, 550))

        # Dibujar inventario al final
        self.inventario.dibujar()
        return None
