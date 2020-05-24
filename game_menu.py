from support_classes import Button
from CONFIG import WIDTH,HEIGHT
import pygame

def main_menu(window,font):
    classic_button = Button((WIDTH/2-40,HEIGHT/2+40),(250,100),"Classic Genius",(0,255,70),font,window)
    while True:
        for event in pygame.event.get():
            pass

        pygame.display.update()