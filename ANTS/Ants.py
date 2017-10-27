import pygame
from pygame.locals import *
import random

from ANTS.Ant import *
from ANTS.Food import *

class ants:

    def __init__(self):
        self.width = 800
        self.height = 600

        self.screen = None

        self.objects = []

        for i in range(10):
            self.objects.append(Ant().set_rotation(random.randint(0,360)).set_to_pos((random.randint(0,self.width),random.randint(0,self.height))).set_maxspeed((5,5)))

        for i in range(10):
            self.objects.append(Food().set_rotation(random.randint(0,360)).set_to_pos((random.randint(0,self.width),random.randint(0,self.height))))


        #self.ant_img=pygame.image.load('ant.png')
        #self.myimage = pygame.image.load("ant.png")
        #self.imagerect = self.myimage.get_rect()

    def xyp(self, xy):
        return (self.xp(xy[0]), self.yp(xy[1]))

    def xp(self, x):
        return int(x*(self.width/2.0)+self.width/2.0)

    def yp(self, y):
        return int(y*(self.height/2.0)+self.height/2.0)

    def draw_lines(self, pointlist, color=(255,255,255), thickness=1):
        pointlist = [self.xyp(point) for point in pointlist]
        pygame.draw.lines(self.screen, color, False, pointlist, 1)

    def draw_arc(self, l, t, r, b, color=(255, 255, 255), thickness=1):
        pygame.draw.arc(self.screen, color, (self.xp(l), self.yp(t), self.xp(r)-self.xp(l), self.yp(b)-self.yp(t)), 0, 180, 1)

    def draw_game(self):


        for obj in self.objects:
            obj.draw_to_surface(self.screen)
            if isinstance(obj,Ant):
                obj.move_direction((random.randint(-10,10),random.randint(-10,10)))
                for obj2 in self.objects:
                    if isinstance(obj2,Food) and obj2.collision(obj):

                        obj2.set_to_pos((random.randint(0,self.width),random.randint(0,self.height)))





        pygame.display.flip()

        self.draw_arc(0.1,0.1,0.2,0.2)
        #draw_lines([(),(),()])

    def drawloop(self):
        # Initializing pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Tutorial - listing 4.3")
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 30)

        # Initaialize clock
        clock = pygame.time.Clock()

        # Starting event loop...
        running = 1
        while running:
            # Limit framerate
            clock.tick(20)

            # Clear screen...
            self.screen.fill((0, 0, 0))

            self.draw_game()

            # Get all events
            for event in pygame.event.get():
                # Close application?
                if event.type == QUIT:
                    running = 0

                # Handle keys
                if event.type == KEYDOWN:

                    # Escape: Quit
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))

            # Show screen
            pygame.display.flip()

            # Check, if this is the main file

game = ants()

game.drawloop()