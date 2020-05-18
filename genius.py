import pygame
import numpy
import pygame.gfxdraw
from math import pi,sin,cos


pygame.mixer.pre_init(44100, -16, 2)
pygame.mixer.init()
pygame.init()

circles = []
n = 8
WIDTH,HEIGHT = 1200,800
window = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.quit()