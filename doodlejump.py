import arcade
import random
from platforms import Platform, PlatformJump, PlatformMove, PlatformDisappearance, PlatformDied
from player import Player
from constants import *


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
        self.platforms.append(self.player)

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

        #self.player.update()
        self.platforms.update()

        # Проверка столкновения с платформами (только при падении)
        platform_hit = arcade.check_for_collision_with_list(self.player, self.platforms)
        if platform_hit:
            for platform in platform_hit:
                self.player.velocity_y = platform.break_down(self.player.velocity_y)
                #print(self.player.velocity_y)

        # Движение камеры вверх
        if self.player.center_y > SCREEN_HEIGHT // 2 + self.camera_y:
            diff = self.player.center_y - (SCREEN_HEIGHT // 2 + self.camera_y)
            self.camera_y += diff
            self.score = int(self.camera_y // 10)

        # Добавление новых платформ
        highest_platform = max(self.platforms, key=lambda p: p.center_y)
        high_of_jump = (JUMP_SPEED / GRAVITY) * JUMP_SPEED / 2
        while highest_platform.center_y < self.camera_y + SCREEN_HEIGHT + 100:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = highest_platform.center_y + min((high_of_jump, self.score / 10 + 60))
            rr = random.random()
            if rr < 0.05:
                platform = PlatformJump(x, y)
            elif rr < 0.2:
                platform = PlatformMove(x, y)
            elif rr < self.score / 2000:
                platform = PlatformDisappearance(x, y)
            else:
                platform = Platform(x, y)
            self.platforms.append(platform)
            if random.random() < 0.1 and self.player.velocity_y <= 15:
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = highest_platform.center_y + min((high_of_jump, self.score / 10 + 60)) + 30
                platform = PlatformDied(x, y)
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
