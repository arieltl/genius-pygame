import pygame
import numpy
import pygame.gfxdraw
from math import pi,sin,cos
from pygame.mixer import Sound
class Note(Sound):
    def __init__(self, frequency, volume=.1):
        self.frequency = frequency/2
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        sample_rate = pygame.mixer.get_init()[0]
        period = int(round(sample_rate / self.frequency))
        amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
        return numpy.array([self.frame_value(amplitude,sample_rate,x) for x in range(0, period)]).astype(numpy.int16)
    
    def frame_value(self,amplitude,sample_rate,i):
        return amplitude * numpy.sin(2.0 * numpy.pi * self.frequency * i / sample_rate)

class Point:
    def __init__(self,position):
        self.position = position
        
    def distance_to(self,point):
        return ((self.position[0] - point.position[0])**2 + (self.position[1] - point.position[1])**2) ** (1/2)


class Circle:
    def __init__(self,center,radius,color,frequency):
        self.center = Point(center)
        self.radius = radius
        self.color = pygame.Color(*color)
        self.sound = Note(frequency)

    def colision(self,position):
        return self.center.distance_to(Point(position)) <= self.radius

    def draw(self,window):
        self.color.a = 200
        pygame.gfxdraw.aacircle(window,*self.center.position,self.radius,self.color)
        pygame.gfxdraw.filled_circle(window,*self.center.position,self.radius,self.color)

    def flash(self,window):
        self.color.a = 255
        pygame.gfxdraw.aacircle(window,*self.center.position,self.radius,self.color)
        pygame.gfxdraw.filled_circle(window,*self.center.position,self.radius,self.color)
        self.sound.play(-1,maxtime=1000)


pygame.mixer.pre_init(44100, -16, 2)
pygame.mixer.init()
pygame.init()

circles = []
n = 8
WIDTH,HEIGHT = 1200,800
window = pygame.display.set_mode((WIDTH, HEIGHT))
for i in range(n):
    angle = i*2*pi/n
    x = int(WIDTH/2 + cos(angle+pi/4) * 200)
    y = int(HEIGHT/2 + sin(angle+pi/4) * 200)
    circles.append(Circle((x,y),50,(255,255,255),410))
    

pygame.display.set_caption('Hello World!')

# ----- Inicia estruturas de dados
game = True


def draw_scene():
    window.fill((0, 0, 0))
    for circle in circles:
        circle.draw(window)
game = True
clock = pygame.time.Clock()
FPS = 30
actions_list = []
running_action = False
draw_scene(None)
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
                            action = {"function": draw_scene,"arguments": (None,), "delay":1000}
                            actions_list.append(action)
                            print("teste")
                            
                
                

    # ----- Gera saídas
    
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador


pygame.quit()