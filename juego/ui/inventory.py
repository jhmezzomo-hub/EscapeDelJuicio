import pygame, sys, os
from juego.controlador.rutas import rutas_img
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Inventario:
    def __init__(self, ventana):
        self.ventana = ventana
        self.objetos = {}  # Cambiado a diccionario para guardar objeto:imagen
        self.seleccionado = None
        self.fuente = pygame.font.SysFont("arial", 20)
        
        # Colores
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.GRIS = (50, 50, 50)
        self.AZUL = (70, 130, 180)

    def agregar(self, objeto, nombre_imagen):
        if objeto not in self.objetos:
            try:
                # Cargar imagen del objeto
                path = rutas_img(nombre_imagen, "objetos")
                imagen = pygame.image.load(path).convert_alpha()
                imagen = pygame.transform.scale(imagen, (60, 60))  # Tamaño del icono
                self.objetos[objeto] = imagen
                print(f"Objeto añadido: {objeto}")
            except pygame.error as e:
                print(f"Error al cargar imagen: {e}")
                self.objetos[objeto] = None
        else:
            print(f"Ya tienes {objeto}")

    def usar(self, objeto):
        if objeto in self.objetos:
            print(f"Usaste {objeto}")
            del self.objetos[objeto]  # Cambiado de remove a del para diccionario
            return True
        else:
            print("No tienes ese objeto")
            return False

    def combinar(self, obj1, obj2, nuevo_obj, nueva_img):
        if obj1 in self.objetos and obj2 in self.objetos:
            del self.objetos[obj1]  # Cambiado de remove a del
            del self.objetos[obj2]  # Cambiado de remove a del
            try:
                path = rutas_img(nueva_img, "objetos")
                imagen = pygame.image.load(path).convert_alpha()
                imagen = pygame.transform.scale(imagen, (60, 60))
                self.objetos[nuevo_obj] = imagen
            except pygame.error as e:
                print(f"Error al cargar imagen combinada: {e}")
                self.objetos[nuevo_obj] = None
            print(f"Combinaste {obj1} + {obj2} = {nuevo_obj}")
            return True
        return False

    def dibujar(self):
        alto = self.ventana.get_height()
        ancho = self.ventana.get_width()
        
        # Panel inferior
        pygame.draw.rect(self.ventana, self.GRIS, (0, alto - 100, ancho, 100))
        texto = self.fuente.render("Inventario:", True, self.BLANCO)
        self.ventana.blit(texto, (10, alto - 90))

        # Dibujar objetos
        for i, (obj, imagen) in enumerate(self.objetos.items()):
            x = 150 + i * 100
            y = alto - 80
            rect = pygame.Rect(x, y, 80, 80)

            color = self.AZUL if self.seleccionado == obj else self.BLANCO
            pygame.draw.rect(self.ventana, color, rect, 2)

            if imagen:
                self.ventana.blit(imagen, (x + 10, y + 10))
            else:
                nombre = self.fuente.render(obj, True, self.BLANCO)
                self.ventana.blit(nombre, (x + 5, y + 25))

    def click(self, pos):
        alto = self.ventana.get_height()
        for i, (obj, imagen) in enumerate(self.objetos.items()):
            x = 150 + i * 100
            y = alto - 80
            rect = pygame.Rect(x, y, 80, 80)
            if rect.collidepoint(pos):
                if self.seleccionado == obj:
                    self.usar(obj)
                    self.seleccionado = None
                    return True
                else:
                    self.seleccionado = obj
                    return True
        return False

    def tiene_objeto(self, objeto):
        return objeto in self.objetos