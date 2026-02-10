import arcade
from constants import *
from random import randint


class Platform(arcade.Sprite):
    def __init__(self, x, y, width=80):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = 10
        self.color = arcade.color.BROWN

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)

    def break_down(self, fall):
        if fall < 0:
            return JUMP_SPEED
        else:
            return fall

    def update(self, _):
        pass


class PlatformDisappearance(Platform):

    def __init__(self, x, y, width=80):
        super().__init__(x, y, width=80)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = 10
        self.color = arcade.color.RED

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)

    def break_down(self, fall):
        if fall < 0:
            self.remove_from_sprite_lists()
            self.kill()
            return JUMP_SPEED
        else:
            return fall

    def update(self, _):
        pass


class PlatformJump(Platform):

    def __init__(self, x, y, width=80):
        super().__init__(x, y, width=80)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = 10
        self.color = arcade.color.BLUE

    def break_down(self, fall):
        if fall < 0:
            return SUPER_JUMP_SPEED
        else:
            return fall

    def update(self, _):
        pass


class PlatformMove(Platform):

    def __init__(self, x, y, width=80):
        super().__init__(x, y, width=80)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = 10
        self.color = arcade.color.WHITE
        self.speed = 2.5

    def break_down(self, fall):
        if fall < 0:
            return JUMP_SPEED
        else:
            return fall

    def update(self, _):
        self.center_x += self.speed

        if self.left < 0:
            self.speed = abs(self.speed)
        elif self.right > SCREEN_WIDTH:
            self.speed = -abs(self.speed)


class PlatformDied(Platform):

    def __init__(self, x, y, width=80):
        super().__init__(x, y, width=80)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = 10
        self.color = arcade.color.BLACK

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)

    def break_down(self, fall):
        if fall < 0:
            self.remove_from_sprite_lists()
            self.kill()
            return SUPER_JUMP_SPEED
        else:
            return -9999

    def update(self, _):
        pass

class Monster(arcade.Sprite):

    def __init__(self, x, y, width=80):
        super().__init__(x, y, width=80)
        self.center_x = x
        self.center_y = y
        self.width = 25
        self.height = 25
        self.idle_texture = arcade.load_texture("img/1.png")
        self.texture = self.idle_texture
        self.speed = 2.5

    def draw(self):
        pass

    def break_down(self, fall):
        if fall < 0:
            self.remove_from_sprite_lists()
            self.kill()
            return SUPER_JUMP_SPEED
        else:
            return -9999

    def update(self, _):
        self.center_x += randint(-10, 10)
        self.center_y += randint(-10, 10)
