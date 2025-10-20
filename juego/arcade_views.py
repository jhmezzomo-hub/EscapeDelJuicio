import arcade
import os
from juego.controlador.cargar_config import get_config_sala

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")  # ajustar si tienes carpeta distinta

class BaseRoom(arcade.View):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.config = get_config_sala(nombre)
        self.background = None
        self.player = None
        self.player_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.keys_held = set()
        self.inventory_open = False
        # control state
        self.left = self.right = self.up = self.down = False

    def setup_base(self):
        # fondo: intenta cargar por nombre de config["fondo"], si no usar color
        try:
            fondo_path = os.path.join(ASSETS_DIR, self.config["fondo"])
            self.background = arcade.load_texture(fondo_path)
        except Exception:
            self.background = None
            arcade.set_background_color(arcade.color.BLACK)

        # crear jugador simple (reemplazar por textura real)
        pos = self.config["personaje"]["pos_inicial"]
        w, h = self.config["personaje"].get("tamaño", (32, 48))
        self.player = arcade.SpriteSolidColor(w, h, arcade.color.BLUE)
        self.player.center_x, self.player.center_y = pos
        self.player_list.append(self.player)

        # puertas: en config son rects estilo pygame; convertimos a sprites
        puertas = self.config.get("puertas", {})
        salida = puertas.get("salida")
        volver = puertas.get("volver")
        if salida:
            sprite = arcade.SpriteSolidColor(salida.width, salida.height, arcade.color.BROWN)
            sprite.center_x = salida.x + salida.width/2
            sprite.center_y = salida.y + salida.height/2
            sprite.properties = {"target": self.config.get("siguiente_sala"), "needs_key": False}
            self.door_list.append(sprite)
        if volver:
            sprite = arcade.SpriteSolidColor(volver.width, volver.height, arcade.color.BROWN)
            sprite.center_x = volver.x + volver.width/2
            sprite.center_y = volver.y + volver.height/2
            sprite.properties = {"target": self.config.get("sala_anterior"), "needs_key": False}
            self.door_list.append(sprite)

        # hook para contenido específico
        self.add_content()

    def add_content(self):
        # sobrescribir en subclases
        pass

    def on_show(self):
        self.setup_base()

    def on_draw(self):
        arcade.start_render()
        if self.background:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.obstacle_list.draw()
        self.door_list.draw()
        self.player_list.draw()
        # indicador de interacción
        hits = arcade.check_for_collision_with_list(self.player, self.door_list)
        if hits:
            arcade.draw_text("Presiona E para entrar", SCREEN_WIDTH//2 - 100, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time: float):
        speed = self.config.get("personaje", {}).get("velocidad", 200)
        vx = (-1 if self.left else 0) + (1 if self.right else 0)
        vy = (-1 if self.down else 0) + (1 if self.up else 0)
        self.player.change_x = vx * speed * delta_time
        self.player.change_y = vy * speed * delta_time
        self.player.center_x += self.player.change_x
        self.player.center_y += self.player.change_y

        # aquí puedes añadir colisiones con máscara/obstáculos si migras colision_piso
        # check puertas automáticas (solo ejemplo)
        # ...

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.left = True
        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.right = True
        if key == arcade.key.W or key == arcade.key.UP:
            self.up = True
        if key == arcade.key.S or key == arcade.key.DOWN:
            self.down = True
        if key == arcade.key.E:
            # interacción con puertas
            hits = arcade.check_for_collision_with_list(self.player, self.door_list)
            if hits:
                target = hits[0].properties.get("target")
                if target:
                    # cargar la vista destino
                    if target == "sala2":
                        from juego.arcade_views import Sala2
                        self.window.show_view(Sala2(target))
                    elif target == "inicio":
                        from juego.arcade_views import SalaInicio
                        self.window.show_view(SalaInicio(target))

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.left = False
        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.right = False
        if key == arcade.key.W or key == arcade.key.UP:
            self.up = False
        if key == arcade.key.S or key == arcade.key.DOWN:
            self.down = False

class SalaInicio(BaseRoom):
    def __init__(self, nombre="inicio"):
        super().__init__(nombre)

    def add_content(self):
        # ejemplo: maniquí simple
        man = arcade.SpriteSolidColor(32, 48, arcade.color.GRAY)
        man.center_x = 300
        man.center_y = 150
        self.obstacle_list.append(man)

class Sala2(BaseRoom):
    def __init__(self, nombre="sala2"):
        super().__init__(nombre)

    def add_content(self):
        # posicion inicial distinta
        self.player.center_x = 50
        self.player.center_y = 200
        # puerta de regreso ya manejada por setup_base si config tiene 'volver'
        pass