from game import Game
import pygame

def main():
    while True:
        game=Game()
        restart=game.run()
        if not restart:
            break
    pygame.quit()

if __name__ == "__main__":
    main()
