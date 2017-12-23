from enum import Enum


class BorderMode(Enum):
    DONUT = 1
    SOLID = 2
    BASIC = 3
    NONE = 4


# Simulation parameters
NB_OCCURRENCES = 5
NB_AGENTS = 10
BOX_SIZE = 600
BORDER_MODE = BorderMode.DONUT

# Forces
GRAVITY = True
WAALS = True
SPRING = True
COULOMB = True

# Forces factors
spring_length = 50
coulomb_factor = 5 * 10e2
waals_factor = 10e-33
gravity_factor = 5 * 10e1
spring_factor = 10e-4


