def cargar_sprites_personaje(nombre_carpeta, ancho_pantalla, alto_pantalla, ancho_sprite=120, alto_sprite=200):
    """
    Carga los sprites del personaje y devuelve:
        sprites: dict con 'idle', 'walk_left', 'walk_right'
        rect: rect inicial del personaje centrado
    """
    carpeta = rutas_img(nombre_carpeta)  # ejemplo: img/mc/
    sprites = {
        "idle": [],
        "walk_left": [],
        "walk_right": []
    }

    # Cargar idle (mc_0.png)
    path_idle = os.path.join(carpeta, "mc_0.png")
    if os.path.exists(path_idle):
        img = pygame.image.load(path_idle).convert_alpha()
        img = pygame.transform.scale(img, (ancho_sprite, alto_sprite))
        sprites["idle"].append(img)
    else:
        raise FileNotFoundError(f"No se encontró {path_idle}")

    # Cargar caminar derecha (mc_1.png, mc_2.png, mc_3.png)
    for i in range(1, 4):
        path = os.path.join(carpeta, f"mc_{i}.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (ancho_sprite, alto_sprite))
            sprites["walk_right"].append(img)
        else:
            raise FileNotFoundError(f"No se encontró {path}")

    # Cargar caminar izquierda (mc_4.png, mc_5.png, mc_6.png)
    for i in range(4, 7):
        path = os.path.join(carpeta, f"mc_{i}.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (ancho_sprite, alto_sprite))
            sprites["walk_left"].append(img)
        else:
            raise FileNotFoundError(f"No se encontró {path}")

    # Dibujar todo
    screen.blit(fondo, (0, 0))

    # Dibujar contorno del hexágono (solo si debug está activo)
    if mostrar_contorno:
        pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)

    # Dibujar personaje
    screen.blit(personaje, personaje_rect)

    # Dibujar inventario por encima (solo se muestra si inv.is_open == True dentro de inv.draw)
    inv.draw(screen)

    pygame.display.flip()
    # Rect inicial centrado en pantalla
    rect = sprites["idle"][0].get_rect(center=(ancho_pantalla//2, alto_pantalla - 150))

    return sprites, rect
# Inicializar Pygame
pygame.init()