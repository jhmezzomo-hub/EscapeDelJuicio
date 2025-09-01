# main.py
import pygame
import sys
import random
from sala2 import create_room as create_sala2

pygame.init()

# Ventana
ancho, alto = 800, 600
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Saw game")

# Colores
COLOR_FONDO_DEFAULT = (30, 30, 30)
color_jugador = (50, 200, 50)
color_paredes = (255, 255, 255)
color_puerta = (210, 105, 30)
color_cama = (100, 149, 237)
color_barriles = (165, 42, 42)
color_boton = (70, 130, 180)
color_boton_hover = (100, 160, 210)
color_texto = (255, 255, 255)
color_debug_barril_llave = (0, 255, 0)  
color_enemigo = (255, 0, 0)
color_mesa = (139, 69, 19)  # marrón

# Tamaños y objetos base (plantilla sala 1)
tamaño_barril = 30
plantilla_barriles_sala1 = [
    (200, 300, tamaño_barril, tamaño_barril),
    (400, 400, tamaño_barril, tamaño_barril),
    (600, 250, tamaño_barril, tamaño_barril)
]

tamaño_jugador = 40
x_jugador, y_jugador = 50, alto // 2
velocidad = 5

tamaño_enemigo = 50 
x_enemigo, y_enemigo = ancho - 100, alto // 2
velocidad_enemigo = 3

plantilla_paredes_sala1 = [
    (150, 100, 500, 20),
    (150, 200, 20, 300),
    (630, 200, 20, 300),
    (150, 500, 500, 20)
]

cama = pygame.Rect(45, 280, 60, 80)  # dibujo estático en sala 1
mesa_sala2 = pygame.Rect(250, 200, 300, 120)  # posición y tamaño de la mesa

# Reloj y fuente
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont(None, 50)

# Plantillas de salas (sala1 y sala2 modular)
salas_plantilla = {
    1: {
        "barriles": plantilla_barriles_sala1,
        "paredes": plantilla_paredes_sala1,
        "puerta": (750, alto // 2, 50, 50),   # puerta derecha (hacia sala2)
        "fondo": COLOR_FONDO_DEFAULT,
        "target": 2
    },
    2: {
        "barriles": [],
        "paredes": [],
        "puerta": (0, alto // 2, 50, 50),  # puerta a la izquierda (vuelve a sala 1)
        "fondo": (30, 30, 30),
        "target": 1,
        "enemigo": (x_enemigo, y_enemigo, tamaño_enemigo, tamaño_enemigo)  # enemigo en sala 2
    }
}

# Variables de sala actual
barriles = []
paredes = []
puerta = None
color_fondo = COLOR_FONDO_DEFAULT
sala_actual = 1

# ---- Llave y estado ----
indice_barril_llave = None
tiene_llave = False

def cargar_sala(num):
    """Carga la plantilla (convierte tuplas a pygame.Rect)."""
    global barriles, paredes, puerta, color_fondo, sala_actual
    plantilla = salas_plantilla[num]
    barriles = [pygame.Rect(*b) for b in plantilla["barriles"]]
    paredes = [pygame.Rect(*p) for p in plantilla["paredes"]]
    puerta = pygame.Rect(*plantilla["puerta"])
    color_fondo = plantilla["fondo"]
    sala_actual = num

# Función para verificar colisiones con paredes y barriles (barriles bloquean movimiento)
def verificar_colisiones(rectangulo):
    for barril in barriles:
        if rectangulo.colliderect(barril):
            return True
    for pared in paredes:
        if rectangulo.colliderect(pared):
            return True
    # Colisión con la mesa solo en sala 2
    if sala_actual == 2 and rectangulo.colliderect(mesa_sala2):
        return True
    return False

# Mostrar texto temporal en pantalla
def mostrar_texto(texto, dur_ms=1200):
    ventana.fill(color_fondo)
    fuente_grande = pygame.font.SysFont(None, 74)
    mensaje = fuente_grande.render(texto, True, color_texto)
    ventana.blit(mensaje, ((ancho - mensaje.get_width()) // 2,
                           (alto - mensaje.get_height()) // 2))
    pygame.display.flip()
    pygame.time.wait(dur_ms)

# Botón usado en pantallas
def boton(texto, x, y, ancho_boton, alto_boton):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color_actual = color_boton_hover if x < mouse[0] < x + ancho_boton and y < mouse[1] < y + alto_boton else color_boton
    pygame.draw.rect(ventana, color_actual, (x, y, ancho_boton, alto_boton))
    texto_render = fuente.render(texto, True, color_texto)
    ventana.blit(texto_render, (x + (ancho_boton - texto_render.get_width()) // 2,
                                 y + (alto_boton - texto_render.get_height()) // 2))
    return click[0] and x < mouse[0] < x + ancho_boton and y < mouse[1] < y + alto_boton

# Pantalla inicio
def pantalla_inicio():
    inicio = True
    while inicio:
        ventana.fill(COLOR_FONDO_DEFAULT)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if boton("Jugar", 300, 250, 200, 60):
            inicio = False
        if boton("Salir", 300, 350, 200, 60):
            pygame.quit()
            sys.exit()
        pygame.display.flip()
        reloj.tick(60)

# Pantalla fin (reiniciar o salir)
def pantalla_fin():
    fin = True
    while fin:
        ventana.fill(COLOR_FONDO_DEFAULT)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if boton("Reiniciar", 300, 250, 200, 60):
            fin = False
        if boton("Salir", 300, 350, 200, 60):
            pygame.quit()
            sys.exit()
        pygame.display.flip()
        reloj.tick(60)

# Reiniciar juego (vuelve a sala 1 y aleatoriza la llave)
def reiniciar_juego():
    global x_jugador, y_jugador, tiene_llave, indice_barril_llave
    x_jugador, y_jugador = 50, alto // 2
    tiene_llave = False
    indice_barril_llave = random.randint(0, len(plantilla_barriles_sala1) - 1)
    cargar_sala(1)

# --- Opción A: interacción inflando el rect del barril ---
def tocar_barril(jugador_rect):
    """
    Interactúa si el jugador está cerca del barril (área inflada).
    Si ya tiene la llave, todos los barriles dicen "No hay nada aquí".
    """
    global tiene_llave
    if sala_actual != 1:
        return  # No mostrar nada si no es sala 1

    for i, barril in enumerate(barriles):
        area_interaccion = barril.inflate(20, 20)
        if jugador_rect.colliderect(area_interaccion):
            if tiene_llave:
                mostrar_texto("No hay nada aquí")
            elif i == indice_barril_llave:
                tiene_llave = True
                mostrar_texto("¡Encontraste la llave!")
            else:
                mostrar_texto("No hay nada aquí")
            return  # Solo muestra mensaje si interactuó con un barril
    # Si no tocó ningún barril, no muestra nada

# Interacción con puerta: cambia de sala si corresponde
def interactuar_puerta(jugador_rect):
    global sala_actual, tiene_llave, x_jugador, y_jugador
    if jugador_rect.colliderect(puerta):
        destino = salas_plantilla[sala_actual]["target"]
        if sala_actual == 1:
            # en sala 1 la puerta exige llave
            if tiene_llave:
                mostrar_texto("La llave abre la puerta... entrando")
                cargar_sala(destino)
                x_jugador, y_jugador = 60, alto // 2  # entrar a sala 2 desde la izquierda
            else:
                mostrar_texto("La puerta está cerrada. Necesitas una llave.")
        else:
            # salas distintas pueden tener comportamiento diferente; sala2 tiene target->1
            mostrar_texto("Volviendo a la sala anterior")
            cargar_sala(destino)
            x_jugador, y_jugador = ancho - 120, alto // 2

# Inicialización del juego
pantalla_inicio()
indice_barril_llave = random.randint(0, len(plantilla_barriles_sala1) - 1)
tiene_llave = False
cargar_sala(1)

# --- Variables para enemigo ---
enemigo_rect = pygame.Rect(x_enemigo, y_enemigo, tamaño_enemigo, tamaño_enemigo)
enemigo_activo = False

# Control para evitar múltiples activaciones al mantener E
ultima_interaccion = 0
DEBOUNCE_MS = 200

# Bucle principal
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        # Uso KEYDOWN para E para evitar múltiples activaciones
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
            ahora = pygame.time.get_ticks()
            if ahora - ultima_interaccion > DEBOUNCE_MS:
                jugador_rect = pygame.Rect(x_jugador, y_jugador, tamaño_jugador, tamaño_jugador)
                # primero intentar tocar barril (si hay alguno)
                tocar_barril(jugador_rect)
                # luego intentar puerta (si está en zona)
                interactuar_puerta(jugador_rect)
                ultima_interaccion = ahora
                if sala_actual == 2:
                    enemigo_activo = True
                    dx_enemigo = x_jugador - enemigo_rect.x
                    dy_enemigo = y_jugador - enemigo_rect.y
                    distancia = (dx_enemigo**2 + dy_enemigo**2)**0.5
                    if distancia < 100:
                        if abs(dx) > 2:
                            enemigo_rect.x += velocidad_enemigo if dx_enemigo > 0 else -velocidad_enemigo
                        if abs(dy) > 2:
                            enemigo_rect.y += velocidad_enemigo if dy_enemigo > 0 else -velocidad_enemigo
                    pygame.draw.rect(ventana, color_enemigo, enemigo_rect)
                    jugador_rect = pygame.Rect(x_jugador, y_jugador, tamaño_jugador, tamaño_jugador)
                    if enemigo_rect.colliderect(jugador_rect):
                        mostrar_texto("¡El enemigo te atrapó! Reiniciando...")
                        reiniciar_juego()
                        enemigo_rect.x, enemigo_rect.y = x_enemigo, y_enemigo  # resetear enemigo
                else:
                    enemigo_activo = False
                    enemigo_rect.x, enemigo_rect.y = x_enemigo, y_enemigo  # resetear enemigo                        
    
    # Movimiento y colisiones
    teclas = pygame.key.get_pressed()
    jugador_rect = pygame.Rect(x_jugador, y_jugador, tamaño_jugador, tamaño_jugador)

    if teclas[pygame.K_LEFT] and x_jugador > 0:
        x_jugador -= velocidad
        jugador_rect.x = x_jugador
        if verificar_colisiones(jugador_rect):
            x_jugador += velocidad
    if teclas[pygame.K_RIGHT] and x_jugador < ancho - tamaño_jugador:
        x_jugador += velocidad
        jugador_rect.x = x_jugador
        if verificar_colisiones(jugador_rect):
            x_jugador -= velocidad
    if teclas[pygame.K_UP] and y_jugador > 0:
        y_jugador -= velocidad
        jugador_rect.y = y_jugador
        if verificar_colisiones(jugador_rect):
            y_jugador += velocidad
    if teclas[pygame.K_DOWN] and y_jugador < alto - tamaño_jugador:
        y_jugador += velocidad
        jugador_rect.y = y_jugador
        if verificar_colisiones(jugador_rect):
            y_jugador -= velocidad

    # Dibujar todo
    ventana.fill(color_fondo)
    if sala_actual == 1:
        pygame.draw.rect(ventana, color_cama, cama)
    if sala_actual == 2:
        pygame.draw.rect(ventana, color_mesa, mesa_sala2)  # dibuja la mesa solo en sala 2
    for idx, barril in enumerate(barriles):
        color = color_barriles
        pygame.draw.rect(ventana, color, barril)
    for pared in paredes:
        pygame.draw.rect(ventana, color_paredes, pared)
    pygame.draw.rect(ventana, color_puerta, puerta)
    pygame.draw.rect(ventana, color_jugador, (x_jugador, y_jugador, tamaño_jugador, tamaño_jugador))

    # --- Enemigo solo en sala 2 ---
    if sala_actual == 2:
        # Activar enemigo solo en sala 2
        enemigo_activo = True
        # Calcular distancia al jugador
        dx = x_jugador - enemigo_rect.x
        dy = y_jugador - enemigo_rect.y
        distancia = (dx**2 + dy**2) ** 0.5
        # Si está cerca, el enemigo persigue al jugador
        if distancia < 300:
            velocidad_enemigo = 4
            # Movimiento en X
            nuevo_rect_x = enemigo_rect.copy()
            if abs(dx) > 2:
                nuevo_rect_x.x += velocidad_enemigo if dx > 0 else -velocidad_enemigo
                if not nuevo_rect_x.colliderect(mesa_sala2):
                    enemigo_rect.x = nuevo_rect_x.x
            # Movimiento en Y
            nuevo_rect_y = enemigo_rect.copy()
            if abs(dy) > 2:
                nuevo_rect_y.y += velocidad_enemigo if dy > 0 else -velocidad_enemigo
                if not nuevo_rect_y.colliderect(mesa_sala2):
                    enemigo_rect.y = nuevo_rect_y.y
        pygame.draw.rect(ventana, color_enemigo, enemigo_rect)
        jugador_rect = pygame.Rect(x_jugador, y_jugador, tamaño_jugador, tamaño_jugador)
        if enemigo_rect.colliderect(jugador_rect):
            mostrar_texto("¡Te atrapó el enemigo!")
            reiniciar_juego()
            enemigo_rect.x, enemigo_rect.y = x_enemigo, y_enemigo
    else:
        enemigo_activo = False
        enemigo_rect.x, enemigo_rect.y = x_enemigo, y_enemigo

    # Indicadores e info
    texto_sala = fuente.render(f"Sala {sala_actual}", True, color_texto)
    ventana.blit(texto_sala, (10, 10))
    
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()


