import pygame.freetype, sys

from juego.controlador.cargar_fondos import cargar_fondo
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla

COLOR_FONDO_DEFAULT = (30, 30, 30)
color_fondo = COLOR_FONDO_DEFAULT

def tutorial():
     size = tamaño_pantallas()
     screen = info_pantalla()
    #  screen.fill(color_fondo)
     # Intentar cargar fondo específico del tutorial (opcional)
     try:
         bg = cargar_fondo("pantalla_tutorial.png", "Fondos")
     except Exception:
         bg = None
 
     clock = pygame.time.Clock()
     fuente = pygame.freetype.SysFont("Arial", 26)
     titulo_fuente = pygame.freetype.SysFont("impact", 64, bold=True)
 
     def render_texto(fuente_local, texto, color, center, outline_size=3):
         surf = pygame.Surface((700, 140), pygame.SRCALPHA)
         surf.fill((0, 0, 0, 0))
         outline_color = (0, 0, 0)
         offsets = [(x, y) for x in [-outline_size, 0, outline_size] for y in [-outline_size, 0, outline_size]]
         for ox, oy in offsets:
             if ox != 0 or oy != 0:
                 fuente_local.render_to(surf, (outline_size + ox, outline_size + oy), texto, fgcolor=outline_color, bgcolor=None)
         fuente_local.render_to(surf, (outline_size, outline_size), texto, fgcolor=color, bgcolor=None)
         return surf, surf.get_rect(center=center)
 
     # Crear botón "VOLVER"
     volver_surf, volver_rect = render_texto(titulo_fuente, "VOLVER", (170, 20, 20), (120, size[1] - 60))
     volver_mask = pygame.mask.from_surface(volver_surf)
 
     instrucciones = [
         "Movimiento: WASD / Flechas",
         "Interactuar: E",
         "Para realizar acciones: Selecciona cualquier objeto en el inventario y pulsa E cerca de una zona interactiva.",
         "Objetivo: Escapar del juicio agarrando objetos y resolviendo puzzles.",
         "",
         "Pulsa ESC para volver al menú"
     ]
 
     running = True
     while running:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
             if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                 running = False
             if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                 mx, my = pygame.mouse.get_pos()
                 if volver_rect.collidepoint((mx, my)):
                     lx = mx - volver_rect.x
                     ly = my - volver_rect.y
                     if 0 <= lx < volver_surf.get_width() and 0 <= ly < volver_surf.get_height():
                         if volver_mask.get_at((lx, ly)):
                             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                 running = False
 
         # Dibujado
         if bg:
             screen.blit(bg, (0, 0))
         else:
             screen.fill(color_fondo)
 
         titulo_surf, titulo_rect = render_texto(titulo_fuente, "TUTORIAL", (200, 50, 50), (size[0] // 2, 90))
         screen.blit(titulo_surf, titulo_rect)
 
         y0 = 170
         for i, linea in enumerate(instrucciones):
             fuente.render_to(screen, (60, y0 + i * 34), linea, (220, 220, 220))
 
         screen.blit(volver_surf, volver_rect)
 
         pygame.display.flip()
         clock.tick(60)