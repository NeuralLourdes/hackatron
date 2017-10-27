import pygame
from pygame.locals import *
import random
import numpy as np

class game_object(object):

    def __init__(self, image):
        self.image=image
        self.position=(100,100)
        self.size=(50,50)
        self.rotation=0
        self.maxspeed=(0,0)

    def collision(self,gameobj):
        dx=self.position[0]-gameobj.position[0]
        dy=self.position[1]-gameobj.position[1]
        return np.sqrt(dx*dx+dy*dy)<50

    def set_maxspeed(self,max_speed):
        self.maxspeed=max_speed
        return self

    def move_direction(self,vector):
        self.position=(self.position[0]+vector[0],self.position[1]+vector[1])
        return self

    def set_rotation(self,rot):
        self.rotation=rot
        return self

    def set_to_pos(self,position):
        self.position=position
        return self

    def moverect(self,rect,xy):
        return (rect[0]+xy[0],rect[1]+xy[1],rect[2]+xy[0],rect[3]+xy[1])


    def draw_to_surface(self,surface):
        rot_img=pygame.transform.rotate(self.image, self.rotation)
        scale_img = pygame.transform.scale(rot_img, self.size)
        surface.blit(scale_img, self.moverect(scale_img.get_rect(), self.position))