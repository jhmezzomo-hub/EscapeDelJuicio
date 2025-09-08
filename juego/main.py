import sys
import os

# Añadir el directorio raíz del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar la función específica que inicia la sala
from juego.salas.salas_inicio import iniciar_sala

def main():
    """Función principal que inicia el juego."""
    print("Iniciando juego desde main.py...")
    iniciar_sala()
    print("Juego terminado.")

# Ejecutar la función main solo si este archivo es el punto de entrada
if __name__ == '__main__':
    main()