import pygame, sys
from juego.pantalla.mensaje_bienvenida import bienvenida_textos

def sala_mensaje_bienvenida():
	pygame.init()
	size = (1100, 600)
	screen = pygame.display.set_mode(size)
	fondo_negro = pygame.Surface(size)
	fondo_negro.fill((0, 0, 0))

	# Cargar personaje (puedes cambiar por el que quieras)
	personaje = pygame.Surface((80, 120))
	personaje.fill((100, 100, 100))
	personaje_rect = personaje.get_rect(center=(size[0]//2, size[1]//2 + 100))
	info_personaje = (personaje, personaje_rect)

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
		mostrar_bienvenida = bienvenida_textos(
			tiempo_actual, tiempo_inicio, fuente, screen, fondo_negro, info_personaje
		)
		clock.tick(60)

if __name__ == "__main__":
	sala_mensaje_bienvenida()