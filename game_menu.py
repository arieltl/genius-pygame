from support_classes import Button
from CONFIG import WIDTH,HEIGHT,COLORS
import pygame

def main_menu(window,font):
    b_width = 300
    b_height = 100
    y_pos0 = HEIGHT/2-(40+b_height)
    x_pos0 = WIDTH/2-(40+b_width)
    y_pos1 = HEIGHT/2 + 40
    x_pos1 = WIDTH/2 + 40
    classic_button = Button(COLORS[0],x_pos0,y_pos0,b_width,b_height,"CLASSIC GENIUS", 50) 
    fast_button = Button(COLORS[1],x_pos1,y_pos0,b_width,b_height,"FAST GENIUS", 50) 
    crazy_button = Button(COLORS[2],x_pos0,y_pos1,b_width,b_height,"CRAZY GENIUS", 50)
    lucianius_button = Button(COLORS[3],x_pos1,y_pos1,b_width,b_height,"LUCIANIUS", 50) 
    
    buttons = [classic_button,fast_button,crazy_button,lucianius_button]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.react_to_mouse(event.pos)
        for button in buttons:
            button.draw(window,(180,180,180))
        pygame.display.update()