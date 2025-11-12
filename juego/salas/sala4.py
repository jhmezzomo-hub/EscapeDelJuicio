import pygame
import sys
import random
import os
import json

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
from juego.controlador.mensaje_paso_sala import devolver_pies_personaje


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
    
    # Cargar imagen de Caperucita feliz para cuando se resuelva el acertijo
    caperucita_feliz_img, _ = cargar_personaje("caperucita_feliz.png", "caperucita", size, personaje_rect.size)
    # Cargar imagen de Caperucita libre (sin cuerdas)
    caperucita_libre_img, _ = cargar_personaje("caperucita_libre.png", "caperucita", size, personaje_rect.size)
    caperucita_img_actual = caperucita_img  # Imagen actual de Caperucita

    # -------- Cargar balde y posicionarlo sobre la cabeza de Caperucita --------
    balde_img, balde_rect = cargar_img("balde.png", "balde", (200, 150))
    balde_rect.midbottom = (caperucita_rect.centerx - 50, caperucita_rect.top - 40)  # -20 para moverlo a la izquierda
    
    # Cargar sprites del balde para la animación
    balde_normal, _ = cargar_img("Balde.png", "balde", (200, 150))
    balde_semiderramado, _ = cargar_img("Balde_semiderramado.png", "balde", (275, 200))
    balde_derramado, _ = cargar_img("Balde_derramado.png", "balde", (285, 200))
    balde_sprites = [balde_normal, balde_semiderramado, balde_derramado]
    balde_img_actual = balde_normal  # Imagen actual del balde
    
    # Hitbox de Caperucita (solo los pies) - ajustada más arriba
    hitbox_caperucita = pygame.Rect(
        caperucita_rect.left + 20,
        caperucita_rect.bottom - 50,  # Subida de 30 a 50 (más arriba)
        caperucita_rect.width - 40,
        30
    )
    
    # Crear hitbox para los pies de Messi usando la función estándar
    pies_personaje = devolver_pies_personaje(personaje_rect)

    maniquies = []
    obstaculos = [{"hitbox": hitbox_caperucita}]
    print("[DEBUG] Sala 4 cargada correctamente con colisiones y objetos visuales.")

    # -------- Mensaje en la pared del fondo --------
    # Cargar acertijos del archivo JSON
    try:
        ruta_acertijos = os.path.join(parent_dir, "data", "acertijos.json")
        with open(ruta_acertijos, 'r', encoding='utf-8') as f:
            acertijos = json.load(f)
        # Seleccionar un acertijo aleatorio
        acertijo_clave = random.choice(list(acertijos.keys()))  # Guardar la clave (respuesta)
        mensaje_pared_texto = acertijos[acertijo_clave]  # El acertijo (pregunta)
        print(f"[DEBUG] Acertijo seleccionado: {mensaje_pared_texto}")
        print(f"[DEBUG] Respuesta correcta: {acertijo_clave}")
    except Exception as e:
        print(f"[ERROR] No se pudo cargar acertijos: {e}")
        mensaje_pared_texto = "Este es un mensaje secreto en la pared"  # Mensaje por defecto
        acertijo_clave = "secreto"  # Respuesta por defecto
    
    mensaje_pared_rect = pygame.Rect(500, 200, 150, 100)  # Cambia posición (x, y) y tamaño (ancho, alto)
    mensaje_pared_mostrado = False  # Controla si se está mostrando el mensaje
    mensaje_pared_timer = 0.0  # Temporizador para mostrar el mensaje
    mensaje_pared_duracion = 3.0  # Tiempo que se muestra el mensaje (en segundos)
    prev_en_mensaje_pared = False  # Para detectar cuando entra/sale del área
    
    # Variables para el input de respuesta
    respuesta_usuario = ""  # Texto que el usuario escribe
    respuesta_correcta = False  # Si adivinó el acertijo
    mensaje_resultado = ""  # Mensaje de correcto/incorrecto
    color_resultado = (255, 255, 255)  # Color del mensaje resultado
    
    # Variables para animación de desvanecimiento
    opacidad_objetos = 255  # Opacidad inicial (0-255)
    desvaneciendo = False  # Si está en proceso de desvanecimiento
    velocidad_desvanecimiento = 200  # Opacidad por segundo que se reduce
    
    # Variables para liberación de Caperucita
    caperucita_liberada = False  # Si Caperucita fue liberada
    mostrar_mensaje_liberar = False  # Si está cerca para liberar
    mensaje_agradecimiento_mostrado = False  # Si se mostró el mensaje de agradecimiento
    mensaje_agradecimiento_timer = 0.0  # Temporizador para el mensaje de agradecimiento
    caperucita_desapareciendo = False  # Si Caperucita está desapareciendo
    opacidad_caperucita = 255  # Opacidad de Caperucita
    velocidad_desvanecimiento_caperucita = 100  # Velocidad de desvanecimiento

    # --- AJO (se crea cuando Caperucita desaparece) ---
    ajo_img = None
    ajo_rect = None
    ajo_obj = None
    ajo_visible = False
    ajo_spawned = False

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
    
    # Variable para detectar si E fue presionada (no mantenida)
    e_presionada_prev = False

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

            # Solo manejar inventario si no está escribiendo la respuesta
            if not mensaje_pared_mostrado:
                inv.handle_event(event)
            
            # Manejar input de texto cuando el mensaje está mostrado
            if mensaje_pared_mostrado and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Verificar respuesta al presionar Enter
                    # Acepta la respuesta si la palabra clave está en la respuesta del usuario
                    respuesta_limpia = respuesta_usuario.lower().strip()
                    if acertijo_clave.lower() in respuesta_limpia:
                        mensaje_resultado = "¡Correcto!"
                        color_resultado = (0, 255, 0)  # Verde
                        respuesta_correcta = True
                        print(f"[DEBUG] ¡Respuesta correcta! ({respuesta_usuario})")
                        # Cerrar automáticamente el mensaje e iniciar desvanecimiento
                        mensaje_pared_mostrado = False
                        mensaje_pared_timer = 0.0
                        respuesta_usuario = ""  # Limpiar respuesta
                        mensaje_resultado = ""  # Limpiar mensaje de resultado
                        desvaneciendo = True  # Iniciar animación de desvanecimiento
                    else:
                        # Respuesta incorrecta: activar secuencia de muerte
                        mensaje_resultado = "Incorrecto..."
                        color_resultado = (255, 0, 0)  # Rojo
                        print(f"[DEBUG] Respuesta incorrecta: {respuesta_usuario}")
                        # Cerrar mensaje y activar animación de muerte
                        mensaje_pared_mostrado = False
                        respuesta_usuario = ""  # Limpiar input
                        mensaje_resultado = ""  # Limpiar mensaje de resultado
                        # Activar secuencia de muerte
                        personaje_bloqueado = True
                        temporizador_muerte = 1.5  # 1.5 segundos para la animación
                        balde_cayendo = True
                        print("[DEBUG] ¡Respuesta incorrecta! El balde va a caer...")
                elif event.key == pygame.K_BACKSPACE:
                    # Borrar último carácter
                    respuesta_usuario = respuesta_usuario[:-1]
                    mensaje_resultado = ""  # Limpiar mensaje de resultado
                elif event.unicode.isprintable() and len(respuesta_usuario) < 30:
                    # Agregar carácter (máximo 30 caracteres)
                    respuesta_usuario += event.unicode
                    mensaje_resultado = ""  # Limpiar mensaje de resultado

        # Movimiento del personaje
        if not inv.is_open and not mensaje_pared_mostrado:  # No permitir movimiento si el mensaje está mostrado
            # Actualizar hitbox de los pies de Messi antes del movimiento
            pies_personaje = devolver_pies_personaje(personaje_rect)
            
            # Actualizar movimiento usando sprites_caminar (bloqueado si personaje_bloqueado)
            current_player_surf = sprites_caminar(
                size, screen, inv, mask, obstaculos, personaje_rect.size, personaje, personaje_rect,
                disable_movement=personaje_bloqueado
            )
            
            teclas = pygame.key.get_pressed()
            
            # Detectar si E fue presionada (transición de no presionada a presionada)
            e_presionada_ahora = teclas[pygame.K_e]
            e_accion = e_presionada_ahora and not e_presionada_prev
            e_presionada_prev = e_presionada_ahora
            
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif teclas[pygame.K_F1]:
                mostrar_contorno = not mostrar_contorno
            elif e_accion:  # Solo actúa cuando E es PRESIONADA (no mantenida)
                # Interacción con ajo (si spawned y visible) - NO afecta colisiones de movimiento
                if ajo_visible and ajo_rect and pies_personaje.colliderect(ajo_rect):
                    try:
                        from juego.controlador.agregar_inv import agregar_a_inventario
                        try:
                            agregar_a_inventario(ajo_obj, inv)
                        except Exception:
                            agregar_a_inventario(inv, ajo_obj)
                    except Exception:
                        pass
                    ajo_obj["visible"] = False
                    ajo_visible = False
                # Interacción con la puerta de volver
                elif personaje_rect.colliderect(puerta_volver):
                    print("[DEBUG] Volver a sala anterior:", config.get("sala_anterior"))
                    return "siguiente_sala"
                # Interacción con Caperucita para liberarla (solo después de resolver el acertijo)
                elif respuesta_correcta and not caperucita_liberada and opacidad_objetos == 0:
                    # Crear área de detección temporal para la interacción
                    area_interaccion = pygame.Rect(
                        caperucita_rect.left - 50,
                        caperucita_rect.top - 50,
                        caperucita_rect.width + 100,
                        caperucita_rect.height + 100
                    )
                    if personaje_rect.colliderect(area_interaccion):
                        caperucita_liberada = True
                        caperucita_img_actual = caperucita_libre_img
                        mensaje_agradecimiento_mostrado = True
                        mensaje_agradecimiento_timer = 3.0  # Mostrar mensaje por 3 segundos
                        print("[DEBUG] Caperucita liberada!")
                # Interacción con el mensaje de la pared (solo si no ha adivinado)
                elif personaje_rect.colliderect(mensaje_pared_rect) and not personaje_bloqueado and not respuesta_correcta:
                    mensaje_pared_mostrado = True
                    print("[DEBUG] Leyendo mensaje de la pared...")
        
        # Manejar cierre del mensaje de la pared (solo si adivinó correctamente)
        if mensaje_pared_mostrado:
            teclas = pygame.key.get_pressed()
            e_presionada_ahora = teclas[pygame.K_e]
            e_accion = e_presionada_ahora and not e_presionada_prev
            e_presionada_prev = e_presionada_ahora
            
            if e_accion and respuesta_correcta:  # Solo se puede cerrar si adivinó
                mensaje_pared_mostrado = False
                mensaje_pared_timer = 0.0
                respuesta_usuario = ""  # Limpiar respuesta
                mensaje_resultado = ""  # Limpiar mensaje de resultado
                print("[DEBUG] Cerrando mensaje de la pared...")
        
        # Animar desvanecimiento de objetos
        if desvaneciendo:
            opacidad_objetos -= velocidad_desvanecimiento * dt
            if opacidad_objetos <= 0:
                opacidad_objetos = 0
                desvaneciendo = False
                # Cambiar a Caperucita feliz cuando el balde desaparece
                caperucita_img_actual = caperucita_feliz_img
                print("[DEBUG] Objetos completamente desvanecidos - Caperucita feliz")
        
        # Manejar mensaje de agradecimiento y desvanecimiento de Caperucita
        if mensaje_agradecimiento_mostrado:
            mensaje_agradecimiento_timer -= dt
            if mensaje_agradecimiento_timer <= 0:
                mensaje_agradecimiento_mostrado = False
                caperucita_desapareciendo = True
                print("[DEBUG] Iniciando desvanecimiento de Caperucita")
        
        # Animar desvanecimiento de Caperucita
        if caperucita_desapareciendo:
            opacidad_caperucita -= velocidad_desvanecimiento_caperucita * dt
            if opacidad_caperucita <= 0:
                opacidad_caperucita = 0
                caperucita_desapareciendo = False
                print("[DEBUG] Caperucita ha desaparecido")
                # --- Spawn del ajo en la posición de Caperucita sin colisionar con el jugador ---
                ajo_img_tmp, ajo_rect_tmp = cargar_img("ajo.png", "objetos", (40, 40))
                ajo_img = ajo_img_tmp
                ajo_rect = ajo_rect_tmp
                # Intentar varias posiciones alrededor de Caperucita hasta que no colisione con el jugador ni con su hitbox
                candidato_base = caperucita_rect.midbottom
                offsets = [(0,0), (0,-50), (0,50), (50,0), (-50,0), (30,-30), (-30,-30), (60,-20), (-60,-20)]
                screen_rect = pygame.Rect(0, 0, size[0], size[1])

                def _no_colision_con_jugador_o_caperucita(r):
                    if r.colliderect(personaje_rect):
                        return False
                    if hitbox_caperucita and r.colliderect(hitbox_caperucita):
                        return False
                    return True

                placed = False
                for dx, dy in offsets:
                    ajo_rect.midbottom = (candidato_base[0] + dx, candidato_base[1] + dy)
                    # ajustar dentro de pantalla
                    ajo_rect.clamp_ip(screen_rect)
                    if _no_colision_con_jugador_o_caperucita(ajo_rect):
                        placed = True
                        break
                if not placed:
                    # fallback: colocarlo encima de Caperucita sin bloquear (intentar arriba)
                    ajo_rect.midbottom = (candidato_base[0], candidato_base[1] - 60)
                    ajo_rect.clamp_ip(screen_rect)

                # Crear también la superficie para el inventario que requiere la clave 'surf_inv'
                try:
                    surf_inv = pygame.transform.scale(ajo_img.copy(), (40, 40))
                except Exception:
                    # fallback: usar la imagen tal cual si no se puede escalar
                    surf_inv = ajo_img

                ajo_obj = {
                    "surf_suelo": ajo_img,
                    "surf_inv": surf_inv,
                    "rect": ajo_rect,
                    "visible": True,
                    "nombre": "ajo",
                    "type": "objetos"
                }
                ajo_visible = True
                ajo_spawned = True
                print("[DEBUG] Ajo creado en la posición de Caperucita (no colisionante)")

                # --- Quitar la hitbox de Caperucita para que desaparezca también (sin colisionar) ---
                try:
                    # filtrar la lista de obstaculos para eliminar la entrada asociada
                    obstaculos = [o for o in obstaculos if o.get("hitbox") is not hitbox_caperucita]
                except Exception:
                    pass
                # anular la referencia para evitar usos futuros
                hitbox_caperucita = None

        # Detectar si está cerca de Caperucita para mostrar mensaje de liberar
        # Crear un área de detección más grande alrededor de Caperucita
        area_deteccion_caperucita = pygame.Rect(
            caperucita_rect.left - 50,
            caperucita_rect.top - 50,
            caperucita_rect.width + 100,
            caperucita_rect.height + 100
        )
        
        if respuesta_correcta and not caperucita_liberada and opacidad_objetos == 0:
            mostrar_mensaje_liberar = personaje_rect.colliderect(area_deteccion_caperucita)
            if mostrar_mensaje_liberar:
                print("[DEBUG] Cerca de Caperucita - mostrando mensaje liberar")
        else:
            mostrar_mensaje_liberar = False
        
        # --- VERIFICAR COLISIÓN CON LA LÍNEA (solo si no ha adivinado el acertijo) ---
        if not personaje_bloqueado and not respuesta_correcta:
            px, py = personaje_rect.center
            x1, y1 = punto_inicio
            x2, y2 = punto_fin
            dist = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1) / ((y2 - y1)**2 + (x2 - x1)**2) ** 0.5
            
            # Si toca la línea, bloquear y activar temporizador
            if dist < 5:
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
                        # Ajustar posición del balde según el sprite actual
                        if indice_sprite_balde == 0:  # Balde normal (200x150)
                            balde_rect.midbottom = (caperucita_rect.centerx - 60, caperucita_rect.top - 40)
                        elif indice_sprite_balde == 1:  # Balde semiderramado (275x200)
                            balde_rect.midbottom = (caperucita_rect.centerx - 70, caperucita_rect.top - 40)
                        elif indice_sprite_balde == 2:  # Balde derramado (275x200)
                            balde_rect.midbottom = (caperucita_rect.centerx - 50, caperucita_rect.top - 40)
                    else:
                        # Mantener en el último sprite (derramado)
                        balde_img_actual = balde_sprites[-1]
                        balde_rect.midbottom = (caperucita_rect.centerx - 50, caperucita_rect.top - 40)
            
            # Cuando se cumple el tiempo, mueres
            if temporizador_muerte <= 0:
                pantalla_fin()
                return

        # Actualizar inventario
        inv.update(dt)

        # Dibujar fondo
        screen.blit(fondo, (0, 0))

        # Dibujar línea límite (a la izquierda de Caperucita) - con opacidad
        if opacidad_objetos > 0:
            try:
                # Crear superficie temporal para la línea con transparencia
                linea_surface = pygame.Surface(size, pygame.SRCALPHA)
                color_linea = (255, 0, 0, int(opacidad_objetos))
                pygame.draw.line(linea_surface, color_linea, punto_inicio, punto_fin, 2)
                screen.blit(linea_surface, (0, 0))
            except Exception:
                pass

        # Dibujar contornos si están activados
        if mostrar_contorno:
            pygame.draw.rect(screen, (0, 255, 255), personaje_rect, 1)
            pygame.draw.rect(screen, (255, 0, 0), puerta_volver, 2)
            pygame.draw.rect(screen, (255, 255, 0), caperucita_rect, 1)
            # Hitbox de Caperucita (si todavía existe)
            if hitbox_caperucita:
                try:
                    pygame.draw.rect(screen, (0, 255, 0), hitbox_caperucita, 1)
                except Exception:
                    pass
            pygame.draw.rect(screen, (255, 165, 0), mensaje_pared_rect, 2)  # Área del mensaje en la pared
            pygame.draw.rect(screen, (0, 255, 255), pies_personaje, 2)  # Hitbox de Messi (pies)
            # Mostrar área de detección de Caperucita si el acertijo está resuelto
            if respuesta_correcta and opacidad_objetos == 0 and not caperucita_liberada:
                area_deteccion_debug = pygame.Rect(
                    caperucita_rect.left - 50,
                    caperucita_rect.top - 50,
                    caperucita_rect.width + 100,
                    caperucita_rect.height + 100
                )
                pygame.draw.rect(screen, (255, 0, 255), area_deteccion_debug, 2)  # Magenta para área de detección

        # Mostrar mensaje temporal si corresponde
        if mensaje_timer > 0:
            mensaje_timer -= dt
            texto_msg = fuente.render(mensaje_texto, True, (255, 255, 255))
            screen.blit(texto_msg, (size[0] // 2 - texto_msg.get_width() // 2, size[1] - 40))
        else:
            mensaje_texto = ""

        # Dibujar personaje principal (animado) solo si no está bloqueado ni leyendo mensaje
        if not personaje_bloqueado and not mensaje_pared_mostrado:
            current_player_surf = sprites_caminar(
                size, screen, inv, mask, obstaculos, personaje_rect.size, personaje, personaje_rect,
                disable_movement=False
            )

        # Dibujar objetos con ordenamiento por profundidad (basado en posición Y)
        # Crear lista de objetos a dibujar con sus posiciones Y
        objetos_a_dibujar = []
        
        # Agregar balde si tiene opacidad
        if opacidad_objetos > 0:
            balde_con_alpha = balde_img_actual.copy()
            balde_con_alpha.set_alpha(int(opacidad_objetos))
            objetos_a_dibujar.append(('balde', balde_con_alpha, balde_rect, caperucita_rect.bottom))
        
        # Agregar Caperucita (usar la imagen actual con opacidad)
        if opacidad_caperucita > 0:
            caperucita_con_alpha = caperucita_img_actual.copy()
            caperucita_con_alpha.set_alpha(int(opacidad_caperucita))
            objetos_a_dibujar.append(('caperucita', caperucita_con_alpha, caperucita_rect, caperucita_rect.bottom))
        
        # Agregar ajo si existe y es visible
        if ajo_visible and ajo_img and ajo_rect:
            objetos_a_dibujar.append(('ajo', ajo_img, ajo_rect, ajo_rect.bottom))
        
        # Agregar jugador
        objetos_a_dibujar.append(('jugador', current_player_surf, personaje_rect, personaje_rect.bottom))
        
        # Ordenar por posición Y (menor Y se dibuja primero = más atrás)
        objetos_a_dibujar.sort(key=lambda x: x[3])
        
        # Dibujar en orden
        for nombre, superficie, rect, _ in objetos_a_dibujar:
            screen.blit(superficie, rect)

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
        
        # --- MENSAJE DE LA PARED (DIBUJADO AL FINAL, SOBRE TODO) ---
        # Detectar si el personaje está cerca del mensaje en la pared
        en_mensaje_pared = personaje_rect.colliderect(mensaje_pared_rect)
        
        # Crear overlay para textos con fondo
        overlay = pygame.Surface(size, pygame.SRCALPHA)
        
        # Mostrar indicador de interacción (solo si no ha adivinado)
        if en_mensaje_pared and not personaje_bloqueado and not mensaje_pared_mostrado and not respuesta_correcta:
            texto_interaccion = fuente.render("Presiona E para leer", True, (255, 255, 255))
            texto_rect = texto_interaccion.get_rect(center=(size[0] // 2, size[1] - 80))
            overlay.blit(texto_interaccion, texto_rect)
        
        # Mostrar mensaje para liberar a Caperucita
        if mostrar_mensaje_liberar:
            texto_liberar = fuente.render("Presiona E para quitar cuerdas", True, (255, 255, 255))
            texto_rect_liberar = texto_liberar.get_rect(center=(size[0] // 2, size[1] - 80))
            overlay.blit(texto_liberar, texto_rect_liberar)
        
        # Mostrar mensaje de agradecimiento de Caperucita
        if mensaje_agradecimiento_mostrado:
            # Fondo semi-transparente
            fondo_agradecimiento = pygame.Rect(size[0] // 2 - 250, size[1] // 2 - 50, 500, 100)
            pygame.draw.rect(overlay, (0, 0, 0, 200), fondo_agradecimiento)
            
            # Texto de agradecimiento
            texto_agradecimiento = fuente.render("Caperucita: ¡Gracias por liberarme!", True, (255, 255, 255))
            texto_agr_rect = texto_agradecimiento.get_rect(center=(size[0] // 2, size[1] // 2))
            overlay.blit(texto_agradecimiento, texto_agr_rect)
        
        # Mostrar mensaje de la pared si fue activado (se mantiene hasta presionar E de nuevo)
        if mensaje_pared_mostrado:
            # Dibujar fondo semi-transparente para el mensaje (toda la franja)
            fondo_mensaje = pygame.Rect(0, size[1] // 2 - 150, size[0], 300)
            pygame.draw.rect(overlay, (0, 0, 0, 200), fondo_mensaje)
            
            # Dibujar el texto del mensaje (acertijo)
            texto_mensaje = fuente.render(mensaje_pared_texto, True, (255, 255, 255))
            texto_msg_rect = texto_mensaje.get_rect(center=(size[0] // 2, size[1] // 2 - 60))
            overlay.blit(texto_mensaje, texto_msg_rect)
            
            # Dibujar caja de input
            input_width = 400
            input_height = 40
            input_rect = pygame.Rect(size[0] // 2 - input_width // 2, size[1] // 2, input_width, input_height)
            pygame.draw.rect(overlay, (50, 50, 50, 255), input_rect)
            pygame.draw.rect(overlay, (150, 150, 150, 255), input_rect, 2)
            
            # Dibujar texto del usuario en la caja
            texto_input = fuente.render(respuesta_usuario + "|", True, (255, 255, 255))
            overlay.blit(texto_input, (input_rect.x + 10, input_rect.y + 8))
            
            # Dibujar instrucción
            texto_instruccion = fuente.render("Escribe tu respuesta y presiona Enter", True, (200, 200, 200))
            texto_instruccion_rect = texto_instruccion.get_rect(center=(size[0] // 2, size[1] // 2 - 30))
            overlay.blit(texto_instruccion, texto_instruccion_rect)
            
            # Mostrar resultado (correcto/incorrecto)
            if mensaje_resultado:
                texto_resultado = fuente.render(mensaje_resultado, True, color_resultado)
                texto_resultado_rect = texto_resultado.get_rect(center=(size[0] // 2, size[1] // 2 + 60))
                overlay.blit(texto_resultado, texto_resultado_rect)
            
            # Indicador para cerrar el mensaje (solo si adivinó)
            if respuesta_correcta:
                texto_cerrar = fuente.render("Presiona E para cerrar", True, (200, 200, 200))
                texto_cerrar_rect = texto_cerrar.get_rect(center=(size[0] // 2, size[1] // 2 + 100))
                overlay.blit(texto_cerrar, texto_cerrar_rect)
        
        # Indicador para ajo (si está cerca)
        # Asegurarse de tener pies_personaje actualizado
        pies_personaje = devolver_pies_personaje(personaje_rect)
        if ajo_visible and ajo_rect and pies_personaje.colliderect(ajo_rect):
            texto_ajo = fuente.render("Presiona E para recoger ajo", True, (255, 255, 255))
            texto_rect_ajo = texto_ajo.get_rect(center=(size[0] // 2, size[1] - 120))
            overlay.blit(texto_ajo, texto_rect_ajo)

        # Aplicar el overlay a la pantalla (DESPUÉS de dibujar todo)
        screen.blit(overlay, (0, 0))
        
        prev_en_mensaje_pared = en_mensaje_pared

        pygame.display.flip()


if __name__ == "__main__":
    iniciar_sala4(crear_inventario())
