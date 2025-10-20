import arcade
from juego.arcade_views import SalaInicio

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "EscapeDelJuicio - Arcade"

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    inicio = SalaInicio("inicio")
    window.show_view(inicio)
    arcade.run()

if __name__ == "__main__":
    main()