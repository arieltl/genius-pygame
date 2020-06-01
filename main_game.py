import pygame
import numpy
import pygame.gfxdraw
from random import randint
from math import pi,sin,cos
from support_classes import Circle, Note
from CONFIG import HEIGHT,WIDTH, DRAW_RADIUS, COLORS, FREQUENCIES, QUIT, END

class GeniusGame:
    def __init__(self, window, manager):
        self.window = window
        self.manager = manager

        
    def start_game(self):
        print("startGame")
        self.sequence = []
        self.input_sequence = []
        self.circles = []
        self.actions_list = []
        self.current_index = 0
        self.awaiting_input = False
        self.difficulty = self.manager.difficulty
        self.waiting_time = 300
        self.flash_time = 1000
        return self.game_loop()


    def increment_sequence(self):
        round = len(self.sequence)
        if self.difficulty[1] and round % 1 == 0 and round !=0 and len(self.circles) < 8:
            print("one more")
            next_i = len(self.circles)
            self.circles.append(Circle(50,COLORS[next_i],FREQUENCIES[next_i]))
            print(round)
            print(COLORS[round])
            self.calculate_scene()
            self.draw_scene()
        if self.difficulty[0] and round % 1 == 0 and round !=0:
            self.flash_time = int(self.flash_time * (0.85 if self.flash_time > 400 else 1))
            self.waiting_time = int(self.waiting_time * (0.95 if self.waiting_time > 200 else 1))
        
        self.sequence.append(randint(0, len(self.circles)-1))
        self.play_sequence()
        

   
    def play_sequence(self):
        actions = []
        for i in self.sequence:
            action = {"function": self.circles[i].flash, "arguments": (self.window, self.flash_time), "delay": self.waiting_time}
            action2 = {"function": self.draw_scene, "delay": self.flash_time}
            
            actions.append(action)
            actions.append(action2)
        await_input = {"function": self.enable_input, "arguments": (True,), "delay": 0}
        self.actions_list += actions + [await_input]

    def new_input(self, circle):
        self.enable_input(False)
        if self.circles.index(circle) == self.sequence[self.current_index]:
            circle.flash(self.window, 300)
            await_input = {"function": self.enable_input, "arguments": (True,), "delay": 0}
            action = {"function": self.draw_scene, "delay":300}
            self.actions_list += [action,await_input]
            self.current_index += 1
            if self.current_index == len(self.sequence):
                self.current_index = 0
                action = {"function": self.increment_sequence, "delay":500}
                self.actions_list.append(action)
        else:
            self.window.fill((255,0,0))
            action = {"function":self.start_game,"delay":1000}
            self.actions_list.append(action)
            


    
    def enable_input(self,enable):
        self.awaiting_input = enable

    def calculate_scene(self):
        for i, circle in enumerate(self.circles):
            angle = i*2*pi/len(self.circles) + pi/4
            x = int(WIDTH/2 + cos(angle) * DRAW_RADIUS)
            y = int(HEIGHT/2 + sin(angle) * DRAW_RADIUS)
            #circles.append(Circle((x,y),50,(255,255,255),410))
            circle.move_to((x, y))

    def draw_scene(self):
            self.window.fill((0, 0, 0))
            for circle in self.circles:
                circle.draw(self.window)

    

    def game_loop(self):
        for i in range(4):
            self.circles.append(Circle(50,COLORS[i], FREQUENCIES[i]))
            print(COLORS[i])
        self.calculate_scene()
            
        pygame.display.set_caption('LUCIANIUS!')
        
        clock = pygame.time.Clock()
        FPS = 30
        running_action = False
        self.draw_scene()
        delay = 0
        timer = 0
        self.increment_sequence()

        while True:
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
                if event.type == pygame.QUIT:
                    print("quit")
                    return QUIT
                elif self.awaiting_input and event.type == pygame.MOUSEBUTTONDOWN:
                        # 1 is the left mouse button, 2 is middle, 3 is right.
                        if event.button == 1:
                            
                            for circle in self.circles:
                                if circle.colision(event.pos):
                                    self.new_input(circle)                
            
            # ----- Atualiza estado do jogo
            pygame.display.update()  # Mostra o novo frame para o jogador
