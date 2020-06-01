import pygame
from pygame.mixer import Sound
import numpy

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
    def __init__(self,radius,color,frequency,center = (0,0)):
        self.center = Point(center)
        self.radius = radius
        self.color = pygame.Color(*color)
        self.sound = Note(frequency)

    def colision(self,position):
        return self.center.distance_to(Point(position)) <= self.radius

    def draw(self,window):
        self.color.a = 200
        pygame.gfxdraw.aacircle(window,*self.center.position,self.radius,(self.color))
        pygame.gfxdraw.filled_circle(window,*self.center.position,self.radius,self.color)

    def flash(self,window, time = 1000):
        self.color.a = 255
        pygame.gfxdraw.aacircle(window,*self.center.position,self.radius+5,(255,255,255))
        pygame.gfxdraw.filled_circle(window,*self.center.position,self.radius+5,(255,255,255))
        pygame.gfxdraw.aacircle(window,*self.center.position,self.radius,self.color)
        pygame.gfxdraw.filled_circle(window,*self.center.position,self.radius,self.color)
        self.sound.play(-1,maxtime = time)

    def move_to(self, position):
        self.center = Point(position)

class Button:
    def __init__(self, color, x,y,width,height, text='', font_size = 50,font_name = None):
        self.color = color
        self.draw_color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font = font_name

    def draw(self,win,outline=None, ):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.draw_color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont(None, self.font_size) if self.font is None else pygame.font.Font(self.font,self.font_size)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

    def react_to_mouse(self,pos):
        if self.isOver(pos):
            self.draw_color = (255,255,255)
        else:
            self.draw_color = self.color

