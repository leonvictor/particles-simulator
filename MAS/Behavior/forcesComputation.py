import numpy as np
import scipy.constants
import scipy.constants as const
import Parameters as param

class ForcesComputation :

    k = 1 / 4 * scipy.constants.pi * scipy.constants.epsilon_0
    spring_length = param.spring_length
    coulomb_factor = param.coulomb_factor
    waals_factor = param.waals_factor
    gravity_factor = param.gravity_factor
    spring_factor = param.spring_factor

    @staticmethod
    def gravity(agent, perceptions):
        interactions = []
        """It's ok to perceive yourself, but not to be attracted by yourself"""
        if agent in perceptions:
            perceptions.remove(agent)
        for p in perceptions:
            norm = np.linalg.norm(agent.position - p.position)
            """this is necessary for not but shouldn't happen anyway"""
            # if p.position.all != agent.position.all:
            if norm != 0:
                gravity = scipy.constants.G * ((agent.mass * p.mass)
                                               / (norm ** 2))

                gravity = gravity * 10e2
                unit_vector = (-agent.position+p.position)/norm
                interactions.append(gravity * unit_vector)

        return np.sum(interactions, axis=0)

    @staticmethod
    def vanDerWaals(agent, perceptions):
        interactions = []
        if agent in perceptions:
            perceptions.remove(agent)
        for p in perceptions:
            norm = np.linalg.norm(agent.position - p.position)
            """this is necessary for not but shouldn't happen anyway"""
            # if p.position.all != agent.position.all:
            if norm != 0:
                """absolute temperature = 0K or -273.15°C or -459.67°F"""
                absolute_temperature = -273.15
                e_keesom = ((agent.dipole_moment ** 2) * (p.dipole_moment ** 2))/(3 * ((4 * const.pi * const.epsilon_0 * agent.environment.relative_permittivity) ** 2) * const.k * absolute_temperature)
                e_debye = (((agent.dipole_moment ** 2) * p.polarizability) + ((p.dipole_moment ** 2) * agent.polarizability))/((4 * const.pi * const.epsilon_0 * agent.environment.relative_permittivity)**2)

                electronic_absorption_frequency = 10
                """ICI : Pas encore trouvé ce que c'est vraiment"""

                e_london = (3/4)*(
                               const.Planck * electronic_absorption_frequency * agent.polarizability * p.polarizability) / ((
                               4 * const.pi * const.epsilon_0)**2)
                vdw = (- 1/(norm**6)) \
                      * (e_keesom + e_debye + e_london)
                vdw = vdw * ForcesComputation.waals_factor
                unit_vector = (agent.position - p.position) / norm
                interactions.append(vdw * unit_vector)
        return np.sum(interactions,axis=0)

    @staticmethod
    def coulomb(agent, perception):
        interactions = []
        """It's ok to perceive yourself, but not to be attracted by yourself"""
        if agent in perception:
            perception.remove(agent)
        for p in perception:
            norm = np.linalg.norm(agent.position - p.position)
            """this is necessary for not but shouldn't happen anyway"""
            # if p.position.all != agent.position.all:
            if norm != 0:
                coulomb = ForcesComputation.k * np.absolute(agent.charge * p.charge) /\
                          (norm ** 2)
                #repulsive force : the vector is away from p
                coulomb *= ForcesComputation.coulomb_factor
                unit_vector = (-p.position + agent.position) / norm
                interactions.append(coulomb * unit_vector)
            else:
                print("norm is 0 !")

        return np.sum(interactions, axis=0)

    @staticmethod
    def spring(agent, perceptions):
        interactions = []
        """It's ok to perceive yourself, but not to be attracted by yourself"""
        if agent in perceptions:
            perceptions.remove(agent)
        for p in perceptions:
            norm = np.linalg.norm(agent.position - p.position)
            """this is necessary for not but shouldn't happen anyway"""
            # if p.position.all != agent.position.all:
            if norm != 0:
                spring = - agent.stiffness * (norm - ForcesComputation.spring_length)
                spring *= ForcesComputation.spring_factor
                unit_vector = (agent.position-p.position)/norm
                interactions.append(spring * unit_vector)

        return np.sum(interactions, axis=0)
