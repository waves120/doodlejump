import arcade
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Doodle Jump"

PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_SPEED = 15
SUPER_JUMP_SPEED = 50


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 40
        self.color = arcade.color.GREEN
        self.velocity_y = 0
        self.velocity_x = 0

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, 20, self.color)
        arcade.draw_circle_filled(self.center_x - 7, self.center_y + 5, 3, arcade.color.BLACK)
        arcade.draw_circle_filled(self.center_x + 7, self.center_y + 5, 3, arcade.color.BLACK)

    def update(self):
        self.center_y += self.velocity_y
        self.center_x += self.velocity_x
        self.velocity_y -= GRAVITY

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH


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

    def break_down(self):
        return JUMP_SPEED

class Platform_Disappearance(Platform):

    def __init__(self, x, y, width=80):
        super().__init__( x, y, width=80)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = 10
        self.color = arcade.color.RED

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)

    def break_down(self):
        self.remove_from_sprite_lists()
        self.kill()
        return JUMP_SPEED


class PlatformJump(Platform):

    def __init__(self, x, y, width=80):
        super().__init__( x, y, width=80)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = 10
        self.color = arcade.color.BLUE

    def brake_down(self):
        return SUPER_JUMP_SPEED



class DoodleJump(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()  # Для интерфейса
        self.player = None
        self.platforms = None
        self.score = 0
        self.game_over = False
        self.camera_y = 0

    def setup(self):
        self.player = Player()
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = 100

        self.platforms = arcade.SpriteList(use_spatial_hash=True)

        # Создаем стартовую платформу
        platform = Platform(SCREEN_WIDTH // 2, 50)
        self.platforms.append(platform)

        # Создаем начальные платформы
        for i in range(10):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = 150 + i * 60
            platform = Platform(x, y)
            self.platforms.append(platform)

        self.score = 0
        self.game_over = False
        self.camera_y = 0

    def on_draw(self):
        self.clear()

        # Используем игровую камеру
        self.camera.use()
        self.camera.position = arcade.math.lerp_2d(self.camera.position, (200, self.camera_y + 300), 0.15)

        # Рисуем платформы и игрока
        self.platforms.draw()
        self.player.draw()

        # Переключаемся на GUI камеру для текста
        self.gui_camera.use()

        # Показываем счёт
        arcade.draw_text(f"Счет: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20, bold=True)

        if self.game_over:
            arcade.draw_text("ИГРА ОКОНЧЕНА", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.RED, 30, anchor_x="center", bold=True)
            arcade.draw_text("Нажмите R для перезапуска", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40,
                             arcade.color.WHITE, 16, anchor_x="center")

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.player.update()

        # Проверка столкновения с платформами (только при падении)
        if self.player.velocity_y < 0:
            platform_hit = arcade.check_for_collision_with_list(self.player, self.platforms)
            if platform_hit:
                for platform in platform_hit:
                    self.player.velocity_y = platform.break_down()
                    print(self.player.velocity_y)

        # Движение камеры вверх
        if self.player.center_y > SCREEN_HEIGHT // 2 + self.camera_y:
            diff = self.player.center_y - (SCREEN_HEIGHT // 2 + self.camera_y)
            self.camera_y += diff
            self.score = int(self.camera_y // 10)

        # Добавление новых платформ
        highest_platform = max(self.platforms, key=lambda p: p.center_y)
        while highest_platform.center_y < self.camera_y + SCREEN_HEIGHT + 100:
            x = random.randint(50, SCREEN_WIDTH - 50)
            high_of_jump = (JUMP_SPEED / GRAVITY) * JUMP_SPEED / 2
            y = highest_platform.center_y + min((high_of_jump,self.score / 10 + 60))
            rr = random.random()
            if rr < self.score / 1700:
                platform = Platform_Disappearance(x, y)
            elif rr < 0.5:
                platform = PlatformJump(x, y)
            else:
                platform = Platform(x, y)
            self.platforms.append(platform)
            highest_platform = platform

        # Удаление платформ за экраном
        for platform in list(self.platforms):
            if platform.center_y < self.camera_y - 50:
                self.platforms.remove(platform)

        # Проверка падения
        if self.player.center_y < self.camera_y - 50:
            self.game_over = True

    def on_key_press(self, key, modifiers):
        if self.game_over and key == arcade.key.R:
            self.setup()
            return

        if key == arcade.key.LEFT:
            self.player.velocity_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player.velocity_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.velocity_x = 0


def main():
    game = DoodleJump()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

