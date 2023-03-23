import random
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH


class Desacelerar(Sprite):
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(2000, 2500)
        self.rect.y = random.randint(125, 300)

    def update(self, game_speed, des):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            des.pop()

    def draw(self, screen):
        screen.blit(self.image, self.rect)