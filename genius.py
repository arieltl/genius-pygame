import pygame
from main_game import GeniusGame
from CONFIG import WIDTH, HEIGHT, DRAW_RADIUS, INIT, END, QUIT, GAME
from game_menu import main_menu
from game_over_menu import game_over
class GameManager:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2)
        pygame.mixer.init()
        pygame.init()
        self.difficulty = [False, False]
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        game = GeniusGame(window, self)
        state = INIT
        while state != QUIT:
            if state == INIT:
                state = main_menu(window, self)
            elif state == GAME:
                state = game.start_game()
            elif state == END:
                state = game_over(window)
            
        pygame.quit()

if __name__ == "__main__":
    manager = GameManager()
