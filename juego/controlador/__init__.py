# Make controlador a Python package
from . import rutas
from . import cargar_personaje
from . import cargar_fondos
from . import colisiones
from . import controles

# Export commonly used functions directly
from .rutas import rutas_img, rutas_data, rutas_juego
from .cargar_personaje import cargar_personaje
from .cargar_fondos import cargar_fondo
from .colisiones import crear_mascara
from .controles import manejar_mc
