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
    sala_actual = "inicio"
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
        for mod_name in candidates:
            try:
                mod = __import__(mod_name, fromlist=['*'])
            except Exception:
                continue
            for fn in func_names:
                func = getattr(mod, fn, None)
                if callable(func):
                    try:
                        # pasar inventario si la función lo acepta
                        siguiente = func(inv)
                        called = True
                        break
                    except TypeError:
                        # probar sin argumentos
                        siguiente = func()
                        called = True
                        break
            if called:
                break

        # Si no encontramos un init específico, caer a la versión genérica cargar_sala
        if not called:
            try:
                siguiente = cargar_sala(sala_actual, maniquies=[], inv=inv, objetos_sala=[])
            except Exception:
                # si tampoco funciona la carga genérica, terminar
                siguiente = None

        if siguiente is None:
            break
        sala_actual = siguiente

    print("Juego terminado.")
        # Iniciar el juego si se ejecuta directamente
if __name__ == "__main__":
    main()