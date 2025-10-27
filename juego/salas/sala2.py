import pygame, sys
from juego.controlador.rutas import rutas_img
from juego.controlador.inventario import crear_inventario


class Sala2:
    def __init__(self, ventana):
        self.ventana = ventana
        self.inventario = crear_inventario(ventana)
        self.llave_recogida = False
        self.rect_llave = pygame.Rect(100, 200, 50, 50)

        # Carga la imagen de la llave
        try:
            path = rutas_img("llave.png", "objetos")
            self.img_llave = pygame.image.load(path).convert_alpha()
            self.img_llave = pygame.transform.scale(self.img_llave, (50, 50))
        except pygame.error as e:
            print(f"Error cargando imagen de llave: {e}")
            self.img_llave = None

    def actualizar(self, personaje_rect):
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.inventario.click(pos)

        # Dibujar llave si no ha sido recogida
        if not self.llave_recogida and self.img_llave:
            self.ventana.blit(self.img_llave, self.rect_llave)
            if personaje_rect.colliderect(self.rect_llave):
                self.llave_recogida = True
                self.inventario.agregar("Llave", "llave.png")

        # Dibujar inventario al final
        self.inventario.dibujar()