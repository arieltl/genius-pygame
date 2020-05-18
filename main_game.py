import pygame
import numpy
import pygame.gfxdraw
from math import pi,sin,cos
from support_classes import Circle, Note
from CONFIG import HEIGHT,WIDTH, DRAW_RADIUS


circles = []
def draw_scene(window):
        window.fill((0, 0, 0))
        for circle in circles:
            circle.draw(window)

def game_loop(window):
    
    n = 8
    for i in range(n):
        angle = i*2*pi/n
        x = int(WIDTH/2 + cos(angle+pi/4) * 200)
        y = int(HEIGHT/2 + sin(angle+pi/4) * 200)
        circles.append(Circle((x,y),50,(255,255,255),410))
        

    pygame.display.set_caption('Hello World!')


    
    game = True
    clock = pygame.time.Clock()
    FPS = 30
    actions_list = []
    running_action = False
    draw_scene(window)
    delay = 0
    timer = 0
    while game:
        # ----- Trata eventos
        dt = clock.tick(FPS)

        if not running_action and len(actions_list) > 0:
            delay = actions_list[0]["delay"]
            timer = 0
            running_action = True


        if running_action:
            timer += dt
            if timer >= delay:
                action = actions_list[0]
                action["function"](*action["arguments"])
                del actions_list[0]
                running_action = False


        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type in {pygame.KEYUP,pygame.QUIT}:
                game = False
            elif not running_action and event.type == pygame.MOUSEBUTTONUP :
                    # 1 is the left mouse button, 2 is middle, 3 is right.
                    if event.button == 1:
                        
                        for circle in circles:
                            if circle.colision(event.pos):
                                circle.flash(window)
                                action = {"function": draw_scene,"arguments": (window,), "delay":1000}
                                actions_list.append(action)
                                print("teste")
                    
        
        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador
