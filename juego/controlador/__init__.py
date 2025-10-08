# Make controlador a Python package
from juego.controlador.controles import manejar_mc
from juego.limite_colisiones.colision_piso import colision_piso
from juego.controlador.rutas import rutas_img, rutas_data, rutas_juego
from juego.controlador.cargar_personaje import crear_personaje
from juego.controlador.cargar_fondos import cargar_fondo
from juego.limite_colisiones.crear_mascara import crear_mascara