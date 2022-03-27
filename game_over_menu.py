# importa dependências
import pygame
import os 
from CONFIG import WIDTH,HEIGHT,COLORS,QUIT,GAME,INIT,FPS
from screen import GameScreen
from support_classes import Button

#instancia um objeto Sound que contem a música 


class GameOver(GameScreen):

    def __init__(self, window, manager):
        super().__init__(window, manager)
        self.music = pygame.mixer.Sound(os.path.join("sprites","evil_morty.ogg"))
        self.music.set_volume(0.4)

    def setup_screen(self):
        #cria texto GAME OVER
        font_path = os.path.join("sprites","PressStart2P-Regular.ttf")
        font = pygame.font.Font(font_path,80)
        self.text = font.render("GAME OVER",True,COLORS[0])
    
        #dimensões dos botões
        b_width = 370
        b_height = 120
        #coordenadas dos botões
        y_pos = HEIGHT/2-b_height + 100
        x_pos0 = WIDTH/2-(40+b_width)
        x_pos1 = WIDTH/2 + 40
        
        #cria botões
        play_again_b = Button(COLORS[0],x_pos0,y_pos,b_width,b_height,"Play Again",35,font_path)
        main_menu_b = Button(COLORS[0],x_pos1,y_pos,b_width,b_height,"Main Menu",35,font_path)
        self.buttons = [play_again_b,main_menu_b]
  
    def main_loop(self):
        #toca música infinitamente
        self.music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(FPS)
            #apaga o frame e desenha um novo 
            self.window.fill((0,0,0))
            for button in self.buttons:
                button.draw(self.window,(180,180,180))
            self.window.blit(self.text,(WIDTH/2 - self.text.get_width()/2,50))
            #lida com eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return QUIT
                elif event.type == pygame.MOUSEMOTION:
                    #botão reconhece a posição do mouse
                    for button in self.buttons:
                        button.react_to_mouse(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #para de tocar a música 
                    #troca para o menu ou joga de novo
                    if self.buttons[0].isOver(event.pos):
                        self.music.stop()
                        return GAME
                    elif self.buttons[1].isOver(event.pos):
                        self.music.stop()
                        return INIT

            #mostra frame  
            pygame.display.update()

    def initialize(self):
       self.setup_screen()
       return self.main_loop()
        