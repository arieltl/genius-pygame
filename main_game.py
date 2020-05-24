import pygame
import numpy
import pygame.gfxdraw
from random import randint
from math import pi,sin,cos
from support_classes import Circle, Note
from CONFIG import HEIGHT,WIDTH, DRAW_RADIUS, COLORS, FREQUENCIES

class GameManager:
    def __init__(self, window):
        self.window = window

        
    def start_game(self):
        self.sequence = []
        self.input_sequence = []
        self.circles = []
        self.actions_list = []
        self.current_index = 0
        self.awaiting_input = False
        self.game_loop()


    def increment_sequence(self):
        self.sequence.append(randint(0, len(self.circles)-1))
        self.play_sequence()

    def new_input(self, circle):
        if self.circles.index(circle) == self.sequence[self.current_index]:
            circle.flash(self.window, 300)
            action = {"function": self.draw_scene, "delay":300}
            self.actions_list.append(action)
            self.current_index += 1
            if self.current_index == len(self.sequence):
                self.current_index = 0
                action = {"function": self.increment_sequence, "delay":0}
                self.actions_list.append(action)
        else:
            self.window.fill((255,0,0))
            action = {"function":self.start_game,"delay":1000}
            self.actions_list.append(action)


    def play_sequence(self):
        actions = []
        for i in self.sequence:
            action = {"function": self.circles[i].flash, "arguments": (self.window,), "delay": 300}
            action2 = {"function": self.draw_scene, "delay": 1000}
            actions.append(action)
            actions.append(action2)
        self.actions_list += actions

    def draw_scene(self):
            self.window.fill((0, 0, 0))
            for circle in self.circles:
                circle.draw(self.window)

    def calculate_scene(self):
        for i, circle in enumerate(self.circles):
            angle = i*2*pi/len(self.circles) + pi/4
            x = int(WIDTH/2 + cos(angle) * DRAW_RADIUS)
            y = int(HEIGHT/2 + sin(angle) * DRAW_RADIUS)
            #circles.append(Circle((x,y),50,(255,255,255),410))
            circle.move_to((x, y))

    def game_loop(self):
        for i in range(4):
            self.circles.append(Circle(50,COLORS[i], FREQUENCIES[i]))
        self.calculate_scene()
            
        pygame.display.set_caption('LUCIANIUS!')
        
        game = True
        clock = pygame.time.Clock()
        FPS = 30
        running_action = False
        self.draw_scene()
        delay = 0
        timer = 0
        self.increment_sequence()

        while game:
            # ----- Trata eventos
            dt = clock.tick(FPS)

            if not running_action and len(self.actions_list) > 0:
                delay = self.actions_list[0]["delay"]
                timer = 0
                running_action = True


            if running_action:
                timer += dt
                if timer >= delay:
                    action = self.actions_list[0]
                    if "arguments" in action:
                        action["function"](*action["arguments"])
                    else:
                        action["function"]()
                    del self.actions_list[0]
                    running_action = False


            for event in pygame.event.get():
                # ----- Verifica consequências
                if event.type in {pygame.KEYUP,pygame.QUIT}:
                    game = False
                elif not running_action and event.type == pygame.MOUSEBUTTONUP :
                        # 1 is the left mouse button, 2 is middle, 3 is right.
                        if event.button == 1:
                            
                            for circle in self.circles:
                                if circle.colision(event.pos):
                                    self.new_input(circle)                
            
            # ----- Atualiza estado do jogo
            pygame.display.update()  # Mostra o novo frame para o jogador
