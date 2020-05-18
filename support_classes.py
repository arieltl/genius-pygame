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
        pygame.gfxdraw.aacircle(window,*self.center.position,self.radius,self.color)
        pygame.gfxdraw.filled_circle(window,*self.center.position,self.radius,self.color)

    def flash(self,window):
        self.color.a = 255
        pygame.gfxdraw.aacircle(window,*self.center.position,self.radius,self.color)
        pygame.gfxdraw.filled_circle(window,*self.center.position,self.radius,self.color)
        self.sound.play(-1,maxtime=1000)

    def move_to(self, position):
        self.center = Point(position)