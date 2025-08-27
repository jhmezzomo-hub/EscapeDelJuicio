import json
import os

RUTA_JUGADOR = os.path.join(os.path.dirname(__file__), "..", "data", "usuario.json")

def login():
    jugador = {}
    jugador["nombre"] = input("Ingrese nombre: ").strip()

    while True:
        try:
            jugador["edad"] = int(input("Ingrese su edad: ").strip())
            break
        except ValueError:
            print("Por favor ingrese un número válido")

    jugador["ciudad"] = input("Ingrese su ciudad: ").strip()

    print("\n=== Perfil del Jugador ===")
    print(f"Nombre : {jugador['nombre']}")
    print(f"Edad   : {jugador['edad']}")
    print(f"Ciudad : {jugador['ciudad']}")
    print("==========================")

    with open(RUTA_JUGADOR, "w", encoding="utf-8") as archivo:
        json.dump(jugador, archivo, ensure_ascii=False, indent=4)

    return jugador

login()
