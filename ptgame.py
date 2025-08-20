import pygame
import sys
import os 

pygame.init()

# Constantes
ANCHO, ALTO = 800, 600
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AMARILLO = (255, 255, 0)
MARRON = (139, 69, 19)

ESCENARIOS = [(50, 50, 200), (0, 150, 0), (150, 0, 0)]

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego con Menú y Puerta")
fuente = pygame.font.SysFont("Arial", 40)
reloj = pygame.time.Clock()

class Boton:
    def __init__(self, texto, x, y, ancho, alto):
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_normal = GRIS
        self.color_hover = (100, 100, 100)

    def dibujar(self, pantalla):
        mouse = pygame.mouse.get_pos()
        color = self.color_hover if self.rect.collidepoint(mouse) else self.color_normal
        pygame.draw.rect(pantalla, color, self.rect)
        texto_render = fuente.render(self.texto, True, NEGRO)
        pantalla.blit(
            texto_render,
            (self.rect.x + (self.rect.width - texto_render.get_width()) // 2,
             self.rect.y + (self.rect.height - texto_render.get_height()) // 2)
        )

    def clickeado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos)

def menu():
    path = os.path.dirname(__file__)
    path = os.path.join(path, "boton_jugar.png")
    boton_jugar = pygame.image.load()
    boton_jugar = Boton(path)
    boton_salir = Boton("Salir", ANCHO // 2 - 100, ALTO // 2 + 10, 200, 50)

    while True:
        pantalla.fill(BLANCO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if boton_jugar.clickeado(evento):
                juego()
                return
            if boton_salir.clickeado(evento):
                pygame.quit()
                sys.exit()

        boton_jugar.dibujar(pantalla)
        boton_salir.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(FPS)

def juego():
    jugador = pygame.Rect(100, 100, 50, 50)
    velocidad = 5
    color_actual = 0

    # Crear la puerta
    puerta = pygame.Rect(700, 250, 40, 100)  # Posición fija, pero se puede cambiar por random

    en_juego = True
    while en_juego:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    en_juego = False  # Volver al menú

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jugador.x -= velocidad
        if teclas[pygame.K_RIGHT]:
            jugador.x += velocidad
        if teclas[pygame.K_UP]:
            jugador.y -= velocidad
        if teclas[pygame.K_DOWN]:
            jugador.y += velocidad

        # Limitar al área de la pantalla
        jugador.x = max(0, min(jugador.x, ANCHO - jugador.width))
        jugador.y = max(0, min(jugador.y, ALTO - jugador.height))

        # Detectar colisión con la puerta
        if jugador.colliderect(puerta):
            color_actual = (color_actual + 1) % len(ESCENARIOS)
            jugador.x, jugador.y = 100, 100  # Reiniciar posición del jugador
            # Opcional: mover la puerta a otra posición

        # Dibujar fondo y objetos
        pantalla.fill(ESCENARIOS[color_actual])
        pygame.draw.rect(pantalla, MARRON, puerta)  # Puerta
        pygame.draw.rect(pantalla, AMARILLO, jugador)  # Jugador

        pygame.display.flip()

# Iniciar desde el menú
menu()
