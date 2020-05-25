import pygame
from main_game import GameManager
from CONFIG import WIDTH, HEIGHT, DRAW_RADIUS
from game_menu import main_menu


pygame.mixer.pre_init(44100, -16, 2)
pygame.mixer.init()
pygame.init()
font = pygame.font.SysFont(None, 40)
window = pygame.display.set_mode((WIDTH, HEIGHT))
main_menu(window,font)
game = GameManager(window)
game.start_game()

pygame.quit()