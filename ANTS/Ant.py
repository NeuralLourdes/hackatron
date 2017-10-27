import pygame
from pygame.locals import *
import random

from ANTS.game_object import *

antimg = pygame.image.load("images/ant.png")

class Ant(game_object):

    def __init__(self):
        game_object.__init__(self, antimg)
