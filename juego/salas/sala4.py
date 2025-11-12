import pygame
import sys
import random
import os

# Añadir el directorio raíz del proyecto al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import teclas_movimiento
from juego.controlador.sprites_caminar import sprites_caminar
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from juego.controlador.cargar_config import get_config_sala
from juego.controlador.inventario import crear_inventario
from juego.controlador.boton_config import crear_boton_config, abrir_menu_config
from juego.ui.inventory import Item
from juego.limite_colisiones.colision_piso import colision_piso
from juego.controlador.cargar_imagen import cargar_img
from juego.pantalla.pantalla_muerte import pantalla_fin


# ------------------- SALA 4 -------------------
def iniciar_sala4(inv=None):
    """Sala 4: con colisiones, personaje animado y puerta de salida."""
    random.seed()

    # Inventario
    if inv is None:
        inv = crear_inventario()

    # Configuración general
    size = tamaño_pantallas()
    screen = info_pantalla()
    general = get_config_sala("general")
    fuente = general["fuente"]

    # Config de sala 4
    config = get_config_sala("sala4")
    if config is None:
        print("[ERROR] No se encontró configuración para sala4")
        return None

    # Cargar fondo y personaje principal
    fondo = cargar_fondo(config["fondo"], "Fondos")
    personaje, personaje_rect = general["personaje"], general["personaje_rect"]

    # Colisiones del piso + paredes
    mask = colision_piso(size)

    # Botón de configuración
    btn_config = crear_boton_config(size[0] - 140, 20)

    # Variables básicas
    mostrar_contorno = False
    clock = pygame.time.Clock()
    velocidad = 5

    # -------- Puerta de salida (derecha) --------
    puerta_volver = config["puertas"]["salida"]

    # -------- Cargar personaje (Caperucita) --------
    caperucita_img, caperucita_rect = cargar_personaje("caperucita.png", "caperucita", size, personaje_rect.size)
    caperucita_rect.midbottom = (180, personaje_rect.bottom)

    # -------- Cargar balde y posicionarlo sobre la cabeza de Caperucita --------
    balde_img, balde_rect = cargar_img("balde.png", "balde", (200, 150))
    balde_rect.midbottom = (caperucita_rect.centerx, caperucita_rect.top - 40)
    
    # Cargar sprites del balde para la animación
    balde_normal, _ = cargar_img("Balde.png", "balde", (200, 150))
    balde_semiderramado, _ = cargar_img("Balde_semiderramado.png", "balde", (275, 200))
    balde_derramado, _ = cargar_img("Balde_derramado.png", "balde", (275, 200))
    balde_sprites = [balde_normal, balde_semiderramado, balde_derramado]
    balde_img_actual = balde_normal  # Imagen actual del balde
    
    # Hitbox de Caperucita (solo los pies)
    hitbox_caperucita = pygame.Rect(
        caperucita_rect.left + 20,
        caperucita_rect.bottom - 30,
        caperucita_rect.width - 40,
        30
    )

    maniquies = []
    obstaculos = [{"hitbox": hitbox_caperucita}]
    print("[DEBUG] Sala 4 cargada correctamente con colisiones y objetos visuales.")

    # -------- Mensaje en la pared del fondo --------
    # MODIFICA ESTOS VALORES:
    mensaje_pared_texto = "Este es un mensaje secreto en la pared"  # Cambia el texto aquí
    mensaje_pared_rect = pygame.Rect(500, 200, 150, 100)  # Cambia posición (x, y) y tamaño (ancho, alto)
    mensaje_pared_mostrado = False  # Controla si se está mostrando el mensaje
    mensaje_pared_timer = 0.0  # Temporizador para mostrar el mensaje
    mensaje_pared_duracion = 3.0  # Tiempo que se muestra el mensaje (en segundos)
    prev_en_mensaje_pared = False  # Para detectar cuando entra/sale del área

    # --- Línea límite situada a la izquierda de Caperucita ---
    limite_x = caperucita_rect.right + 30
    punto_inicio = (limite_x + 130, 385)
    punto_fin = (limite_x, size[1])
    
    print(f"[DEBUG] Línea límite creada en x = {punto_fin[0]}")

    # Mensajes temporales
    mensaje_texto = ""
    mensaje_timer = 0.0
    mensaje_duracion = 1.0
    
    # Variables para animación de muerte
    personaje_bloqueado = False
    temporizador_muerte = 0.0  # segundos restantes para morir
    balde_cayendo = False
    indice_sprite_balde = 0  # Índice del sprite actual del balde
    tiempo_entre_sprites = 0.5  # Tiempo en segundos entre cada sprite
    temporizador_sprite = 0.0  # Temporizador para cambiar sprites

    # Bucle principal
    while True:
        dt = clock.tick(60) / 1000.0

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            try:
                btn_config.handle_event(event, lambda: abrir_menu_config(screen))
            except Exception:
                pass

            inv.handle_event(event)

        # Movimiento del personaje
        if not inv.is_open:
            # Actualizar movimiento usando sprites_caminar (bloqueado si personaje_bloqueado)
            current_player_surf = sprites_caminar(
                size, screen, inv, mask, obstaculos, personaje_rect.size, personaje, personaje_rect,
                disable_movement=personaje_bloqueado
            )
            
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif teclas[pygame.K_F1]:
                mostrar_contorno = not mostrar_contorno
            elif teclas[pygame.K_e]:
                # Interacción con la puerta de volver
                if personaje_rect.colliderect(puerta_volver):
                    print("[DEBUG] Volver a sala anterior:", config.get("sala_anterior"))
                    return "siguiente_sala"
                
                # Interacción con el mensaje de la pared
                if personaje_rect.colliderect(mensaje_pared_rect) and not personaje_bloqueado:
                    mensaje_pared_mostrado = True
                    mensaje_pared_timer = mensaje_pared_duracion
                    print("[DEBUG] Leyendo mensaje de la pared...")
        
        # --- VERIFICAR COLISIÓN CON LA LÍNEA ---
        if not personaje_bloqueado:
            px, py = personaje_rect.center
            x1, y1 = punto_inicio
            x2, y2 = punto_fin
            dist = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1) / ((y2 - y1)**2 + (x2 - x1)**2) ** 0.5
            
            # Si toca la línea, bloquear y activar temporizador
            if dist < 10:
                personaje_bloqueado = True
                temporizador_muerte = 1.5  # 1.5 segundos para la animación
                balde_cayendo = True
                print("[DEBUG] ¡Tocaste la línea! El balde va a caer...")
        
        # Si está bloqueado, contar tiempo y animar la caída del balde
        if personaje_bloqueado:
            temporizador_muerte -= dt
            
            # Animar sprites del balde
            if balde_cayendo:
                temporizador_sprite += dt
                if temporizador_sprite >= tiempo_entre_sprites:
                    temporizador_sprite = 0.0
                    indice_sprite_balde += 1
                    if indice_sprite_balde < len(balde_sprites):
                        balde_img_actual = balde_sprites[indice_sprite_balde]
                    else:
                        # Mantener en el último sprite (derramado)
                        balde_img_actual = balde_sprites[-1]
            
            # Cuando se cumple el tiempo, mueres
            if temporizador_muerte <= 0:
                pantalla_fin()
                return

        # Actualizar inventario
        inv.update(dt)

        # Dibujar fondo
        screen.blit(fondo, (0, 0))

        # Dibujar línea límite (a la izquierda de Caperucita)
        try:
            pygame.draw.line(screen, (255, 0, 0), punto_inicio, punto_fin, 2)
        except Exception:
            pass

        # Dibujar contornos si están activados
        if mostrar_contorno:
            pygame.draw.rect(screen, (0, 255, 255), personaje_rect, 1)
            pygame.draw.rect(screen, (255, 0, 0), puerta_volver, 2)
            pygame.draw.rect(screen, (255, 255, 0), caperucita_rect, 1)
            pygame.draw.rect(screen, (0, 255, 0), hitbox_caperucita, 1)  # Hitbox de Caperucita
            pygame.draw.rect(screen, (255, 165, 0), mensaje_pared_rect, 2)  # Área del mensaje en la pared

        # Mostrar mensaje temporal si corresponde
        if mensaje_timer > 0:
            mensaje_timer -= dt
            texto_msg = fuente.render(mensaje_texto, True, (255, 255, 255))
            screen.blit(texto_msg, (size[0] // 2 - texto_msg.get_width() // 2, size[1] - 40))
        else:
            mensaje_texto = ""
        
        # --- MENSAJE DE LA PARED ---
        # Detectar si el personaje está cerca del mensaje en la pared
        en_mensaje_pared = personaje_rect.colliderect(mensaje_pared_rect)
        
        # Mostrar indicador de interacción
        if en_mensaje_pared and not personaje_bloqueado and not mensaje_pared_mostrado:
            texto_interaccion = fuente.render("Presiona E para leer", True, (255, 255, 255))
            screen.blit(texto_interaccion, (size[0] // 2 - texto_interaccion.get_width() // 2, size[1] - 80))
        
        # Mostrar mensaje de la pared si fue activado
        if mensaje_pared_mostrado:
            mensaje_pared_timer -= dt
            if mensaje_pared_timer <= 0:
                mensaje_pared_mostrado = False
            else:
                # Dibujar fondo semi-transparente para el mensaje
                overlay = pygame.Surface((size[0], 200), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, size[1] // 2 - 100))
                
                # Dibujar el texto del mensaje (puedes ajustar el tamaño de fuente si quieres)
                texto_mensaje = fuente.render(mensaje_pared_texto, True, (255, 255, 255))
                screen.blit(texto_mensaje, (size[0] // 2 - texto_mensaje.get_width() // 2, size[1] // 2))
        
        prev_en_mensaje_pared = en_mensaje_pared

        # Dibujar personaje principal (animado) solo si no está bloqueado
        if not personaje_bloqueado:
            current_player_surf = sprites_caminar(
                size, screen, inv, mask, obstaculos, personaje_rect.size, personaje, personaje_rect,
                disable_movement=False
            )

        # Dibujar objetos (balde, Caperucita y jugador)
        if personaje_rect.bottom > caperucita_rect.bottom:
            screen.blit(balde_img_actual, balde_rect)  # Usar imagen actual del balde
            screen.blit(current_player_surf, personaje_rect)
            screen.blit(caperucita_img, caperucita_rect)
        else:
            screen.blit(balde_img_actual, balde_rect)  # Usar imagen actual del balde
            screen.blit(caperucita_img, caperucita_rect)
            screen.blit(current_player_surf, personaje_rect)

        # Mostrar texto de interacción con la puerta
        if personaje_rect.colliderect(puerta_volver):
            texto = fuente.render("Presiona E para volver a la sala anterior", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        # Dibujar botón de configuración
        try:
            btn_config.draw(screen)
        except Exception:
            pass

        # Dibujar inventario
        try:
            inv.draw(screen)
        except Exception as e:
            print("ERROR al dibujar inventario:", e)

        pygame.display.flip()


if __name__ == "__main__":
    iniciar_sala4(crear_inventario())
