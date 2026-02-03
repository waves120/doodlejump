import arcade
from constants import *


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 40
        self.velocity_y = 0
        self.velocity_x = 0
        self.idle_texture = arcade.load_texture("img/player.png")
        self.texture = self.idle_texture

    def draw(self):
        pass

    def update(self, _):
        self.center_y += self.velocity_y
        self.center_x += self.velocity_x
        self.velocity_y -= GRAVITY

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
