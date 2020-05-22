import pygame
import numpy
import pygame.gfxdraw
from random import randint
from math import pi,sin,cos
from support_classes import Circle, Note
from CONFIG import HEIGHT,WIDTH, DRAW_RADIUS, COLORS, FREQUENCIES

sequence = []
input_sequence = []
circles = []
actions_list = []
current_index = 0
awaiting_input = False

def increment_sequence(window):
    sequence.append(randint(0, len(circles)-1))
    play_sequence(window)

def new_input(circle, window):
    if circles.index(circle) == sequence[current_index]:
        circle.flash(window)
        action = {"function": draw_scene,"arguments": (window,), "delay":1000}
        actions_list.append(action)
        action = {"function": increment_sequence,"arguments": (window,), "delay":0}

def play_sequence(window):
    global actions_list
    actions = []
    for i in sequence:
        action = {"function": circles[i].flash, "arguments": (window,), "delay": 0}
        action2 = {"function": draw_scene, "arguments": (window,), "delay": 1000}
        actions.append(action)
        actions.append(action2)
    actions_list += actions

def draw_scene(window):
        window.fill((0, 0, 0))
        for circle in circles:
            circle.draw(window)

def calculate_scene():
    for i, circle in enumerate(circles):
        angle = i*2*pi/len(circles) + pi/4
        x = int(WIDTH/2 + cos(angle) * DRAW_RADIUS)
        y = int(HEIGHT/2 + sin(angle) * DRAW_RADIUS)
        #circles.append(Circle((x,y),50,(255,255,255),410))
        circle.move_to((x, y))

def game_loop(window):
    
    n = 4
    for i in range(n):
        circles.append(Circle(50,COLORS[i], FREQUENCIES[i]))
    calculate_scene()
        

    pygame.display.set_caption('LUCIANIUS!')


    
    game = True
    clock = pygame.time.Clock()
    FPS = 30
    running_action = False
    draw_scene(window)
    delay = 0
    timer = 0
    increment_sequence(window)

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
                                new_input(circle, window)                
        
        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador
