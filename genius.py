import pygame
import numpy
import pygame.gfxdraw
from math import pi,sin,cos
from main_game import game_loop
from CONFIG import WIDTH, HEIGHT, DRAW_RADIUS

pygame.mixer.pre_init(44100, -16, 2)
pygame.mixer.init()
pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))

game_loop(window)

pygame.quit()