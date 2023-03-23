from dino_runner.utils.constants import DESACELERAR, DESACELERAR_TYPE
from dino_runner.components.powerups.desacelerar import Desacelerar


class Desdel(Desacelerar):
    def __init__(self):
        self.image = DESACELERAR
        self.type = DESACELERAR_TYPE
        super().__init__(self.image, self.type)