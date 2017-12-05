import pygame
from pygame.locals import *

import sgc

from random import uniform
import matplotlib.pyplot as plt

from Environement.environment import Environment


class Gui:

    def init_env(self):
        for i in range(70):
            self.env.addAgent()

    def __init__(self):
        self.env = Environment(2)

        self.init_env()

        # Initialize sliders (and actual starting values) here
        self.current_mass_value = 1
        self.current_charge_value = 1

        pygame.init()

        self.info = pygame.display.Info()
        self.dw = int(self.info.current_w / 3)
        self.dh = int(self.info.current_h / 3)

        self.screen = sgc.surface.Screen((2 * self.dw, 2 * self.dh))

        self.fgColor = (0, 0, 0)
        self.bgColor = (255, 255, 255)

        # Particle mass scale
        self.mass_scale = sgc.Scale(label="Particle mass",
                                    label_side="top",
                                    label_col=self.fgColor,
                                    pos=(10, 20),
                                    min=1,
                                    max=100000000,
                                    min_step=100,
                                    max_step=1000
                                    )
        self.mass_scale.add(0)

        # Particle charge scale
        self.charge_scale = sgc.Scale(label="Particle charge",
                                      label_side="top",
                                      label_col=self.fgColor,
                                      pos=(10, 90),
                                      min=1,
                                      max=100000000,
                                      min_step=100,
                                      max_step=1000
                                      )
        self.charge_scale.add(1)

        # self.fenetre.fill(self.bgColor)
        # self.screen.fill(self.bgColor)

        self.clock = pygame.time.Clock()

        self.listPos = list()

    def run(self):

        continuer = 1

        while continuer:
            time = self.clock.tick()
            # probably better not to update values on each step
            # it will have to do for now !

            self.env.actualize(mass=self.current_mass_value, charge=self.current_charge_value)

            pxarray = pygame.PixelArray(self.screen.image)

            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                sgc.event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continuer = 0
                elif event.type == QUIT:
                    continuer = 0
                elif event.type == MOUSEBUTTONUP:
                    self.current_mass_value = self.mass_scale.value
                    self.current_charge_value = self.charge_scale.value

                    # if self.mass_scale.value != self.current_mass_value:
                    #     print (self.mass_scale.value)

            self.screen.fill(self.bgColor)
            for el in self.env.agentList:
                self.draw_point(el.position, pxarray)
            for el in self.env.objectList:
                self.draw_point(el.position, pxarray)

            del pxarray
            sgc.update(time)
            pygame.display.flip()
        self.show_temperature()

    def show_temperature(self):
        temp = self.env.dataStore.speedList

        plt.plot(list(temp.keys()), temp.values())
        plt.title("Temperature evolution")
        plt.xlabel("time (s)")
        plt.ylabel("temperature")
        plt.show()

    def draw_point(self, pos, pxarray):

        radius = 1
        (x, y) = pos
        x = int(x)
        y = int(y)

        if (x not in range(-self.dw - radius, self.dw - radius)) or (
                y not in range(-self.dh - radius, self.dh - radius)):
            return

        x += self.dw
        y += self.dh

        # pygame.draw.circle(self.fenetre, self.fgColor, (x,y), radius)

        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                pxarray[i, j] = (uniform(5, 10) * 10, uniform(0, 0), uniform(0, 32) * 8)
                # self.pxarray[i, j] = (0, 0, 0)

    def __del__(self):
        pygame.quit()
