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
