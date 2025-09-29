import pygame
import sys
from juego.controlador.salas import cargar_sala_base, actualizar_sala_base

def iniciar_sala2():
    # Cargar elementos base
    elementos = cargar_sala_base("Fondo_sala1.png", "Fondos")
    
    # Elementos específicos de la sala 2
    marron = (139, 69, 19)
    
    # Aquí defines la posición de la puerta - puedes modificar estos valores
    # Los parámetros son: (x, y, ancho, alto)
    puerta = pygame.Rect(725, 220, 180, 180)  # Puerta visual
    puerta_interaccion = pygame.Rect(770, 400, 120, 40)  # Área de interacción

    # Bucle principal de la sala
    while True:
        # Actualizar y dibujar elementos base
        dt = actualizar_sala_base(elementos)
        
        # Dibujar elementos específicos de la sala 2
        pygame.draw.rect(elementos["screen"], marron, puerta)  # Puerta visual
        pygame.draw.rect(elementos["screen"], (255, 0, 0), puerta_interaccion, 2)  # Área de interacción
        
        # Actualizar pantalla
        pygame.display.flip()