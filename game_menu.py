from support_classes import Button
from CONFIG import WIDTH,HEIGHT
import pygame

def main_menu(window,font):
    classic_button = Button((W,0),(200,100),"Classic Genius",(0,255,70),font,window)
    while True:
        for event in pygame.event.get():
            pass

        pygame.display.update()