import pygame
from main_game import GeniusGame
from CONFIG import WIDTH, HEIGHT, DRAW_RADIUS, INIT, END, QUIT, GAME
from game_menu import main_menu
from game_over_menu import game_over

#class que gerencia telas do jogo
class GameManager:
    def __init__(self):

        #incializa pygame
        pygame.mixer.pre_init(44100, -16, 2)
        pygame.mixer.init()
        pygame.init()

        # modificadores de dificuldade do jogo.
        self.difficulty = [False, False]

        window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('LUCIANIUS!')
        #criando um obejto de jogo
        game = GeniusGame(window, self)

        #controle de fluxo das telas do jogo
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
