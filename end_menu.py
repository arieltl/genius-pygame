import pygame

def game_over(window):
    font = pygame.font.Font("/PressStart2P-Regular",58)
    text = font.render("game over",True,(255,0,0))
    window.blit(text,(0,0))
    while True:
        pass
    