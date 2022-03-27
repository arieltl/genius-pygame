#importa dependências 
import pygame
from game_over_menu import GameOver
from main_game import GeniusGame
from CONFIG import WIDTH, HEIGHT, DRAW_RADIUS, INIT, END, QUIT, GAME
from game_menu import MainMenu

import os
import json

from screen import GameScreen

#class que gerencia telas do jogo
class GameManager:
    def __init__(self):

        #incializa pygame
       
        pygame.init()

        #Verifica se existe um JSON com records e se não, o cria
        if not os.path.exists("scores.json"):
            data = { "[True, True]" : 0,
            "[True, False]" : 0,
            "[False, True]" : 0,
            "[False, False]" : 0}
            with open("scores.json", 'w') as file:
                json.dump(data,file,indent=4)

        # modificadores de dificuldade do jogo
        self.difficulty = [False, False]

        #cria janela do app
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('LUCIANIUS!')
        #criando um objeto de jogo
 
        screens = {GAME: GeniusGame(window, self),INIT:MainMenu(window, self),END:GameOver(window,self)}
        #controle de fluxo das telas do jogo
        state = INIT
        while state != QUIT:
            screen: GameScreen = screens[state]
            state = screen.initialize()


        #sai do jogo   
        pygame.quit()

if __name__ == "__main__":
    manager = GameManager()
