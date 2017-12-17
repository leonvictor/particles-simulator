import pygame
from pygame.locals import *

import sgc

from random import uniform
import matplotlib.pyplot as plt
from sgc.widgets._locals import GUI

from Environement.environment import Environment


class Gui:

    def init_env(self):
        if self.env is not None:
            del self.env
        self.env = Environment(self.env_dim)

        for i in range(60):
            self.env.addAgent()

    def __init__(self):

        self.env = None
        self.env_dim = 2

        # Initialize sliders (and actual starting values) here
        self.current_mass_value = 1
        self.current_charge_value = 1
        self.current_dipole_moment = 1
        self.current_polarizability = 1
        self.sim_running = False
        self.nb_sequences = -1

        pygame.init()
        self.info = pygame.display.Info()
        self.dw = int(self.info.current_w/2)
        self.dh = int(self.info.current_h/2)

        self.screen = sgc.surface.Screen((2 * self.dw, 2 * self.dh))

        self.fgColor = (0, 0, 0)
        self.bgColor = (255, 255, 255)

        btn = sgc.Button(label="Run/Pause",
                         pos=(10,self.info.current_h/3 - 20)
                         )

        btn.on_click = self.change_sim_state
        btn.add(5)
        # Particle mass scale
        self.mass_scale = sgc.Scale(label="Particle mass",
                                    label_side="top",
                                    label_col=self.fgColor,
                                    pos=(10, 20),
                                    min=1,
                                    max=100,
                                    min_step=1,
                                    max_step=99
                                    )
        self.mass_scale.add(0)

        # Particle charge scale
        self.charge_scale = sgc.Scale(label="Particle charge",
                                      label_side="top",
                                      label_col=self.fgColor,
                                      pos=(10, 90),
                                      min=1,
                                      max=100,
                                      min_step=1,
                                      max_step=99
                                      )
        self.charge_scale.add(1)

        self.dipole_moment_scale = sgc.Scale(label="Particle dipole moment",
                                             label_side="top",
                                             label_col=self.fgColor,
                                             pos=(10, 160),
                                             min=1,
                                             max=100000000,
                                             min_step=100,
                                             max_step=1000
                                             )
        self.dipole_moment_scale.add(2)

        self.polarizability_scale = sgc.Scale(label="Particle polarizability",
                                              label_side="top",
                                              label_col=self.fgColor,
                                              pos=(10, 230),
                                              min=1,
                                              max=100000000,
                                              min_step=100,
                                              max_step=1000
                                              )
        self.polarizability_scale.add(3)

        # self.fenetre.fill(self.bgColor)
        # self.screen.fill(self.bgColor)

        self.clock = pygame.time.Clock()



    def run_sequence(self):
        continuer = 1
        for mass in range(0, 101, 5):
            if not continuer:
                break
            for charge in range(0, 101, 5):
                if not continuer:
                    break
                for dipole_moment in range(0, 101, 5):
                    if not continuer:
                        break
                    for polarizability in range(0, 101, 5):
                        if not continuer:
                                break

                        continuer = 1
                        self.nb_sequences = 10
                        self.sim_running = True

                        self.init_env()

                        while continuer and (self.nb_sequences != 0):
                            time = self.clock.tick()
                            # probably better not to update values on each step
                            # it will have to do for now !

                            if self.sim_running:
                                self.env.actualize(mass=self.current_mass_value,
                                                   charge=self.current_charge_value,
                                                   polarizability=self.current_polarizability,
                                                   dipole_moment=self.current_dipole_moment)

                            pxarray = pygame.PixelArray(self.screen.image)

                            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                                sgc.event(event)
                                if event.type == GUI:
                                    print(event)
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        continuer = 0
                                elif event.type == QUIT:
                                    continuer = 0
                                elif event.type == MOUSEBUTTONUP:
                                    self.current_mass_value = self.mass_scale.value
                                    self.current_charge_value = self.charge_scale.value
                                    self.current_dipole_moment = self.dipole_moment_scale.value
                                    self.current_polarizability = self.polarizability_scale.value

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

                            if self.nb_sequences > 0:
                                self.nb_sequences -= 1

                        #self.show_temperature()

    def run(self):

        restart = True
        while restart:
            continuer = 1
            restart = False

            self.init_env()

            while continuer and (self.nb_sequences != 0):
                time = self.clock.tick()
                # probably better not to update values on each step
                # it will have to do for now !

                if self.sim_running:
                    self.env.actualize(mass=self.current_mass_value,
                                       charge=self.current_charge_value,
                                       polarizability=self.current_polarizability,
                                       dipole_moment=self.current_dipole_moment)

                pxarray = pygame.PixelArray(self.screen.image)

                for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                    sgc.event(event)
                    if event.type == GUI:
                        print(event)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            continuer = 0
                        if event.key == pygame.K_r:
                            continuer = 0
                            restart = True
                    elif event.type == QUIT:
                        continuer = 0
                    elif event.type == MOUSEBUTTONUP:
                        self.current_mass_value = self.mass_scale.value
                        self.current_charge_value = self.charge_scale.value
                        self.current_dipole_moment = self.dipole_moment_scale.value
                        self.current_polarizability = self.polarizability_scale.value

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

                if self.nb_sequences > 0:
                    self.nb_sequences -= 1

            self.show_temperature()

    def change_sim_state(self):
        self.sim_running = not self.sim_running

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
