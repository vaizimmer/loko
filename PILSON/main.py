import arcade

from src.game import Game

largura = 800
altura = 600

def main():
    game = Game(largura, altura)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()