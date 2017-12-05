import pygame
from random import uniform
from pygame.locals import *
import matplotlib.pyplot as plt

from Environement.environment import Environment


class Gui :

    def initEnv(self):
        for i in range(70):
            self.env.addAgent()

    def __init__(self):
        self.env = Environment(2)

        self.initEnv()

        pygame.init()

        self.info = pygame.display.Info()
        self.dw = int(self.info.current_w / 3)
        self.dh = int(self.info.current_h / 3)
        self.fenetre = pygame.display.set_mode((2*self.dw, 2*self.dh))

        self.bgColor = (255, 255, 255)
        self.fgColor = (0, 0, 0)
        self.fenetre.fill(self.bgColor)
        self.pxarray = pygame.PixelArray(self.fenetre)
        self.listPos = list()



    def run(self):

        continuer = 1

        while continuer:

            self.env.actualize()

            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continuer = 0
                elif event.type == QUIT:
                    continuer = 0

            self.fenetre.fill(self.bgColor)

            for el in self.env.agentList:
                self.drawPoint(el.position)
            for el in self.env.objectList:
                self.drawPoint(el.position)

            pygame.display.update()
        self.showTemperature()

    def showTemperature(self):
        temp = self.env.dataStore.speedList

        plt.plot(list(temp.keys()), temp.values())
        plt.title("Temperature evolution")
        plt.xlabel("time (s)")
        plt.ylabel("temperature")
        plt.show()

    def drawPoint(self, pos):

        radius = 1
        (x, y) = pos
        x = int(x)
        y = int(y)

        if (x not in range(-self.dw-radius, self.dw-radius)) or (y not in range(-self.dh-radius, self.dh-radius)):
            return

        x += self.dw
        y += self.dh

        # pygame.draw.circle(self.fenetre, self.fgColor, (x,y), radius)

        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                self.pxarray[i, j] = (uniform(5,10)*10,uniform(0,0),uniform(0,32)*8)
                # self.pxarray[i, j] = (0, 0, 0)

    def __del__(self):
        pygame.quit()
