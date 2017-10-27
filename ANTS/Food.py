import pygame
from pygame.locals import *
import random

from ANTS.game_object import *

foodimg = pygame.image.load("images/food.png")

class Food(game_object):

    def __init__(self):
        game_object.__init__(self, foodimg)