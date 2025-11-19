import pygame, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.pantalla.pantalla_inicio import pantalla_de_inicio
from juego.salas.cargar_salas import cargar_sala
from juego.salas.sala_mensaje import sala_mensaje_bienvenida
from juego.controlador.inventario import crear_inventario

def main():
    print("Iniciando juego desde main.py...")    
    pygame.init()
    # Inicializar el display antes de cualquier carga de imágenes
    from info_pantalla.info_pantalla import info_pantalla
    screen = info_pantalla()
    inv = crear_inventario()
    pantalla_de_inicio()  # Mostrar menú principal
    sala_actual = "sala7"
    #sala_mensaje_bienvenida()  # Mostrar mensaje de bienvenida
    while True:
        siguiente = None
        # Intentar resolver dinámicamente la función de inicio de sala
        # 1) módulos posibles
        candidates = [
            f'juego.salas.{sala_actual}',
            f'juego.salas.salas_{sala_actual}',
            f'juego.salas.sala_{sala_actual}'
        ]
        # 2) nombres de función probables
        func_names = [f'iniciar_{sala_actual}', f'iniciar_sala_{sala_actual}']

        called = False 
        import inspect
        for mod_name in candidates:
            try:
                mod = __import__(mod_name, fromlist=['*'])
                print(f"[DEBUG] Módulo encontrado: {mod_name}")
            except Exception as e:
                print(f"[DEBUG] Módulo no encontrado: {mod_name} - {e}")
                continue
            for fn in func_names:
                func = getattr(mod, fn, None)
                print(f"[DEBUG] Buscando función: {fn} en {mod_name} - {'ENCONTRADA' if callable(func) else 'NO ENCONTRADA'}")
                if callable(func):
                    # Llamar según la firma de la función para evitar capturar
                    # TypeError que ocurra dentro de la función.
                    try:
                        sig = inspect.signature(func)
                        params = sig.parameters
                        # Si acepta al menos un parámetro posicional o varargs, pasar inv
                        accepts_inv = False
                        for p in params.values():
                            if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                                accepts_inv = True
                                break
                            if p.kind == inspect.Parameter.VAR_POSITIONAL:
                                accepts_inv = True
                                break

                        if accepts_inv:
                            print(f"[DEBUG main] Llamando {fn} en {mod_name} con inv")
                            try:
                                siguiente = func(inv)
                                print(f"[DEBUG main] Función devolvió: '{siguiente}'")
                            except Exception as e:
                                print(f"[DEBUG main] Error ejecutando función: {e}")
                                siguiente = 'None'
                        else:
                            print(f"[DEBUG main] Llamando {fn} en {mod_name} sin inv")
                            try:
                                siguiente = func()
                                print(f"[DEBUG main] Función devolvió: '{siguiente}'")
                            except Exception as e:
                                print(f"[DEBUG main] Error ejecutando función: {e}")
                                siguiente = 'None'
                        called = True
                        break
                    except Exception as e:
                        # Si algo falla al inspeccionar o llamar, mostrar debug y continuar
                        print(f"[DEBUG] Error llamando {fn} en {mod_name}: {e}")
                        continue
            if called:
                break

        # Si no encontramos un init específico, caer a la versión genérica cargar_sala
        if not called:
            try:
                siguiente = cargar_sala(sala_actual, maniquies=[], inv=inv, objetos_sala=[])
            except Exception:
                # si tampoco funciona la carga genérica, terminar
                siguiente = None

        print(f"[DEBUG] Valor de siguiente: '{siguiente}'")
        
        if siguiente is None or siguiente == 'None':
            print("[DEBUG] siguiente es None o 'None', terminando juego")
            break
        
        # Manejar casos especiales de retorno
        if siguiente == 'inicio' or siguiente == 'menu':
            print(f"[DEBUG] Detectado {siguiente}, volviendo al menú desde sala normal")
            # Volver al menú principal (desde sala normal)
            pantalla_de_inicio()
            # Después del menú, reiniciar desde sala7
            sala_actual = "sala7"
            continue  # Continuar el bucle en lugar de terminar
        elif siguiente == 'menu_victoria':
            # Volver al menú principal (desde pantalla de victoria)
            print("[DEBUG] Detectado menu_victoria, mostrando pantalla de inicio")
            pantalla_de_inicio()
            # Después del menú, iniciar desde la sala inicio
            print("[DEBUG] Configurando sala_actual = 'inicio'")
            sala_actual = "inicio"
            continue  # Continuar el bucle
        
        print(f"[DEBUG] Configurando sala_actual = '{siguiente}'")
        sala_actual = siguiente

    print("Juego terminado.")
        # Iniciar el juego si se ejecuta directamente
if __name__ == "__main__":
    main()