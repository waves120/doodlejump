import arcade
from doodlejump import DoodleJump


def main():
    game = DoodleJump()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
