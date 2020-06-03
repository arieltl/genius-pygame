import pygame
import os 
from CONFIG import WIDTH,HEIGHT,COLORS,QUIT,GAME,INIT,FPS
from support_classes import Button

music = pygame.mixer.Sound(os.path.join("sprites","evil_morty.ogg"))
music.set_volume(0.4)

def game_over(window):
    font_path = os.path.join("sprites","PressStart2P-Regular.ttf")
    font = pygame.font.Font(font_path,80)
    text = font.render("GAME OVER",True,COLORS[0])
   
    b_width = 370
    b_height = 120
    y_pos = HEIGHT/2-b_height + 100
    x_pos0 = WIDTH/2-(40+b_width)
    x_pos1 = WIDTH/2 + 40
    
    play_again_b = Button(COLORS[0],x_pos0,y_pos,b_width,b_height,"Play Again",35,font_path)
    main_menu_b = Button(COLORS[0],x_pos1,y_pos,b_width,b_height,"Main Menu",35,font_path)
    buttons = [play_again_b,main_menu_b]

    music.play(-1)
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        window.fill((0,0,0))
        for button in buttons:
            button.draw(window,(180,180,180))
        window.blit(text,(WIDTH/2 - text.get_width()/2,50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.react_to_mouse(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_b.isOver(event.pos):
                    music.stop()
                    return GAME
                elif main_menu_b.isOver(event.pos):
                    music.stop()
                    return INIT
            
        pygame.display.update()
    