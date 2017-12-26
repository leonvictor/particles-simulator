from enum import Enum


class BorderMode(Enum):
    DONUT = 1
    SOLID = 2
    BASIC = 3
    NONE = 4


# Simulation parameters
DIMENSIONS = 2
NB_OCCURRENCES = 5
NB_AGENTS = 10
BOX_SIZE = 600
BORDER_MODE = BorderMode.SOLID
DELTA_TIME = 0.05
PERCEPTION_RADIUS = 500

#Environment
DIMENSION = 2
GRID_SIZE = 50
TIME_STEP = 0.1

# Forces
GRAVITY = True
WAALS = True
SPRING = False
COULOMB = True

# Forces factors
spring_length = 50
coulomb_factor = 5 * 10e2
waals_factor = 10e-33
gravity_factor = 5 * 10e1
spring_factor = 10e-4


