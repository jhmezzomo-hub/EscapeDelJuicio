import pygame, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.pantalla.mensaje_enfrentamiento import enfrentamiento_textos
from juego.controlador.cargar_fondos import cargar_fondo

def sala_mensaje_bienvenida():
	pygame.init()
	size = (1100, 600)
	screen = pygame.display.set_mode(size)
	"""
	fondo_negro = pygame.Surface(size)
	fondo_negro.fill((0, 0, 0))
	"""

	fondo = cargar_fondo("pantalla_saw_2.png", "saw")

	fuente = pygame.font.SysFont("Arial", 26)
	tiempo_inicio = pygame.time.get_ticks()
	mostrar_bienvenida = True
	clock = pygame.time.Clock()
	while mostrar_bienvenida:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		tiempo_actual = pygame.time.get_ticks()
		mostrar_bienvenida = enfrentamiento_textos(
			tiempo_actual, tiempo_inicio, fuente, screen, fondo 
		)
		clock.tick(60)

if __name__ == "__main__":
	sala_mensaje_bienvenida()