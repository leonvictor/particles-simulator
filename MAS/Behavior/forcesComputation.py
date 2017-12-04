import numpy as np
import scipy.constants
import scipy.constants as const

class ForcesComputation :

    @staticmethod
    def gravity(agent, perceptions):
        interactions = []
        """It's ok to perceive yourself, but not to be attracted by yourself"""
        if agent in perceptions:
            perceptions.remove(agent)
        for p in perceptions:
            """this is necessary for not but shouldn't happen anyway"""
            #if p.position.all != agent.position.all:
            gravity = scipy.constants.G * ((agent.mass * p.mass) / (np.linalg.norm(agent.position - p.position)) ** 2)
            unit_vector = (-agent.position+p.position)/np.linalg.norm(agent.position-p.position)
            interactions.append(gravity * unit_vector)

        return np.sum(interactions, axis=0)

    @staticmethod
    def vanDerWaals(agent, perceptions):
        interactions = []
        if agent in perceptions:
            perceptions.remove(agent)
        for p in perceptions:

            """absolute temperature = 0K or -273.15°C or -459.67°F"""
            absolute_temperature = -273.15
            e_keesom = ((agent.dipole_moment ** 2) * (p.dipole_moment ** 2))/(3 * ((4 * const.pi * const.epsilon_0 * agent.environment.relative_permittivity) ** 2) * const.k * absolute_temperature)
            e_debye = (((agent.dipole_moment ** 2) * p.polarizability) + ((p.dipole_moment ** 2) * agent.polarizability))/((4 * const.pi * const.epsilon_0 * agent.environment.relative_permittivity)**2)

            electronic_absorption_frequency = 10
            """ICI : Pas encore trouvé ce que c'est vraiment"""

            e_london = (3/4)*(
                           const.Planck * electronic_absorption_frequency * agent.polarizability * p.polarizability) / ((
                           4 * const.pi * const.epsilon_0)**2)
            vdw = (- 1/(np.linalg.norm(agent.position - p.position)**6)) * (e_keesom + e_debye + e_london)

            unit_vector = (agent.position - p.position) / np.linalg.norm(agent.position - p.position)
            interactions.append(vdw * unit_vector)
        return np.sum(interactions,axis=0)

    @staticmethod
    def coulomb(agent, perception, k):
        interactions = []
        """It's ok to perceive yourself, but not to be attracted by yourself"""
        if agent in perception:
            perception.remove(agent)
        for p in perception:
            """this is necessary for now but shouldn't happen anyway"""
            #if p.position.all != agent.position.all:
            coulomb = k * np.absolute(agent.charge * p.charge) / (np.linalg.norm(p.position - agent.position) ** 2)
            #repulsive force : the vector is away from p
            unit_vector = (-p.position + agent.position) * np.linalg.norm(p.position - agent.position)
            interactions.append(coulomb * unit_vector)


        return np.sum(interactions, axis=0)
