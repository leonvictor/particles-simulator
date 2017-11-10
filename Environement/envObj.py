from Others.vector import Vector

class EnvObj:
    """Classe représentant un objet de l'environnement"""

    def __init__(self, environment):
        self._position = Vector(*((0.0,)*environment.dimension))
        self.environment = environment


