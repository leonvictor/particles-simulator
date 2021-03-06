import numpy as np
import scipy.constants
import scipy.constants as const
import Parameters as param


class ForcesComputation:
    keesom_const = (3 * ((4 * const.pi * const.epsilon_0 * 1.0006) ** 2) * const.k * -273.15)
    debye_const = ((4 * const.pi * const.epsilon_0 * 1.0006) ** 2)
    electronic_absorption_frequency = 10
    london_const = (3 / 4) * const.Planck * electronic_absorption_frequency / ((4 * const.pi * const.epsilon_0) ** 2)
    k = 1 / 4 * scipy.constants.pi * scipy.constants.epsilon_0

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

                gravity = gravity * param.GRAVITY_FACTOR
                unit_vector = (-agent.position + p.position) / norm
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
                e_keesom = ((agent.dipole_moment ** 2) * (p.dipole_moment ** 2)) / ForcesComputation.keesom_const
                e_debye = (((agent.dipole_moment ** 2) * p.polarizability) + (
                        (p.dipole_moment ** 2) * agent.polarizability)) / ForcesComputation.debye_const

                e_london = ForcesComputation.london_const * (agent.polarizability * p.polarizability)
                vdw = (- 1 / (norm ** 6)) * (e_keesom + e_debye + e_london)
                vdw = vdw * param.WAALS_FACTOR
                unit_vector = (agent.position - p.position) / norm
                interactions.append(vdw * unit_vector)
        return np.sum(interactions, axis=0)

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
                coulomb = ForcesComputation.k * np.absolute(agent.charge * p.charge) / \
                          (norm ** 2)
                # repulsive force : the vector is away from p
                coulomb *= param.COULOMB_FACTOR
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
                spring = agent.stiffness * (norm - param.SPRING_LENGTH)
                spring *= param.SPRING_FACTOR
                unit_vector = (p.position - agent.position ) / norm
                interactions.append(spring * unit_vector)

        return np.sum(interactions, axis=0)
