import pygame
from pygame.locals import *

import sgc

import matplotlib.pyplot as plt
from sgc.widgets._locals import GUI

import Parameters as param
from Environment.environment import Environment


class Gui:

    def init_env(self):
        if self.env is not None:
            del self.env
        self.env = Environment()
        for i in range(param.NB_AGENTS):
            self.env.add_agent()

    def __init__(self):

        # initialisation dans le run
        self.env = None

        # Initialize sliders (and actual starting values) here
        self.current_mass_value = 1
        self.current_charge_value = 1
        self.current_dipole_moment = 1
        self.current_polarizability = 1
        self.current_stiffness = 1
        self.sim_running = False
        self.nb_sequences = -1

        pygame.init()
        pygame.display.init()

        self.info = pygame.display.Info()
        self.dw = int(self.info.current_w / 3)
        self.dh = int(self.info.current_h / 3)
        self.screen = sgc.surface.Screen((2 * self.dw, 2 * self.dh))
        self.fgColor = (0, 0, 0)
        self.bgColor = (255, 255, 255)

        btn = sgc.Button(label="Run/Pause",
                         pos=(10, self.info.current_h / 3 - 20)
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
                                      min=0,
                                      max=100,
                                      min_step=1,
                                      max_step=100
                                      )
        self.charge_scale.add(1)

        self.dipole_moment_scale = sgc.Scale(label="Particle dipole moment",
                                             label_side="top",
                                             label_col=self.fgColor,
                                             pos=(10, 160),
                                             min=0,
                                             max=100,
                                             min_step=1,
                                             max_step=100
                                             )
        self.dipole_moment_scale.add(2)

        self.polarizability_scale = sgc.Scale(label="Particle polarizability",
                                              label_side="top",
                                              label_col=self.fgColor,
                                              pos=(10, 230),
                                              min=0,
                                              max=100000,
                                              min_step=1,
                                              max_step=99999
                                              )
        self.polarizability_scale.add(3)

        self.stiffness_scale = sgc.Scale(label="Stiffness",
                                         label_side="top",
                                         label_col=self.fgColor,
                                         pos=(10, 300),
                                         min=0,
                                         max=100,
                                         min_step=1,
                                         max_step=100
                                         )
        self.stiffness_scale.add(3)

        self.clock = pygame.time.Clock()

    def run_params(self, mass, charge, polarizability, dipole_moment, nb_sequences):
        """Run the session with the indicated parameters, if no data exists for entropy, create some"""

        data = Environment.get_probability_grid_config(mass, charge, polarizability, dipole_moment, nb_sequences)

        if data is None:
            self.run_sequence(mass, charge, polarizability, dipole_moment, nb_sequences)

        self.nb_sequences = nb_sequences
        params = (mass, charge, polarizability, dipole_moment)

        (self.mass_scale.value, self.charge_scale.value, self.dipole_moment_scale.value,
         self.polarizability_scale.value) = params

        self.run(params)

    def run_sequence(self, mass, charge, polarizability, dipole_moment, stiffness, nb_sequences):
        ranges_list = (range(mass, mass + 1), range(charge, charge + 1), range(polarizability, polarizability + 1),
                       range(dipole_moment, dipole_moment + 1), range(stiffness, stiffness + 1))
        self.run_sequence_ranges(ranges_list, nb_sequences)

    def run_sequence_ranges(self, params_ranges_list, nb_sequences):
        continuer = 1

        configurations = Environment.build_list(params_ranges_list)

        for configuration in configurations:
            if not continuer:
                break
            continuer = 1

            (mass, charge, polarizability, dipole_moment, stiffness) = configuration
            for i in range(0, param.NB_OCCURRENCES):
                if not continuer:
                    break

                self.nb_sequences = nb_sequences
                self.init_env()
                while continuer and (self.nb_sequences != 0):
                    self.env.actualize(mass=mass,
                                       charge=charge,
                                       polarizability=polarizability,
                                       dipole_moment=dipole_moment,
                                       stiffness=stiffness)
                    if self.nb_sequences > 0:
                        self.nb_sequences -= 1
        self.nb_sequences = -1

    def run(self, params=None):

        restart = True
        if params is not None:
            (self.current_mass_value, self.current_charge_value,
             self.current_polarizability, self.current_dipole_moment, self.current_stiffness) = params

        while restart:
            self.init_env()
            continuer = 1
            self.env.data_store.clear()
            while continuer and (self.nb_sequences != 0):

                # probably better not to update values on each step
                # it will have to do for now !

                if self.sim_running:
                    self.env.actualize(mass=self.current_mass_value,
                                       charge=self.current_charge_value,
                                       polarizability=self.current_polarizability,
                                       dipole_moment=self.current_dipole_moment,
                                       stiffness=self.current_stiffness)
                    if self.nb_sequences > 0:
                        self.nb_sequences -= 1

                continuer, restart = self.pygame_event_managing(params is None)
                self.pygame_display_managing()

            plt.subplot(4, 2, 1)
            self.draw_dict("Temperature", self.env.data_store.temperature)
            plt.subplot(4, 2, 2)
            self.draw_dict("Volume", self.env.data_store.volume)
            plt.subplot(4, 2, 3)
            self.draw_dict("Pressure", self.env.data_store.pressure)
            plt.subplot(4, 2, 4)
            self.draw_dict("Entropy", self.env.data_store.entropy)
            plt.subplot(4, 2, 5)
            self.draw_dict_f_dict(self.env.data_store.temperature, self.env.data_store.pressure,
                                  "temperature", "pressure")
            plt.subplot(4, 2, 6)
            self.draw_dict_f_dict(self.env.data_store.volume, self.env.data_store.pressure,
                                  "volume", "pressure")
            plt.subplot(4, 2, 7)
            self.draw_dict("Pressure (borders)", self.env.data_store.border_collision_range,
                           name_x="Time (" + str(param.DELTA_TIME*param.RANGE_COLLISIONS_GRAPH) + " s)")
            plt.subplot(4, 2, 8)
            self.draw_dict("Partition function", self.env.data_store.free_energy, show=True)

    def pygame_display_managing(self):
        time = self.clock.tick()
        self.screen.fill(self.bgColor)
        pxarray = pygame.PixelArray(self.screen.image)
        for el in self.env.agent_list:
            self.draw_point(el.position, pxarray, el.color)
        for el in self.env.object_list:
            self.draw_point(el.position, pxarray)
        del pxarray
        sgc.update(time)

        if (param.BORDER_MODE != param.BorderMode.NONE):
            pygame.draw.rect(self.screen.image, self.fgColor, (self.dw - param.BOX_SIZE / 2,
                                                               self.dh - param.BOX_SIZE / 2,
                                                               param.BOX_SIZE,
                                                               param.BOX_SIZE), 1)
        pygame.display.flip()

    def pygame_event_managing(self, param_change_allowed):
        continuer = 1
        restart = False
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
            elif event.type == MOUSEBUTTONUP and param_change_allowed:
                self.current_mass_value = self.mass_scale.value
                self.current_charge_value = self.charge_scale.value
                self.current_dipole_moment = self.dipole_moment_scale.value
                self.current_polarizability = self.polarizability_scale.value
                self.current_stiffness = self.stiffness_scale.value
        return continuer, restart

    def change_sim_state(self):
        self.sim_running = not self.sim_running

    def draw_dict(self, name, dict, name_x=None, show=False):
        if len(dict) != 0:
            plt.plot(list(dict.keys()), dict.values())
            plt.title(name + " evolution")
            if name_x is None:
                plt.xlabel("Time (" + str(param.DELTA_TIME) + " s)")
            else:
                plt.xlabel(name_x)
            plt.ylabel(name)
            if show:
                plt.show()

    def draw_all(self, dict_list):

        for dict in dict_list:
            plt.plot(list(dict.keys()), dict.values())
        plt.title("All")
        plt.xlabel("Time (" + str(self.env.deltaTime) + " s)")
        plt.ylabel("All")
        plt.show()

    def draw_dict_f_dict(self, dict, dict2, name, name2, show=False):
        result = {}

        for k in dict.keys():
            result[dict[k]] = dict2[k]

        self.draw_dict(name, result, name2, show=show)

    def draw_point(self, pos, pxarray, color = (0, 0, 0)):

        radius = param.PARTICULE_RADIUS
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
                pxarray[i, j] = color

    def __del__(self):
        pygame.quit()
