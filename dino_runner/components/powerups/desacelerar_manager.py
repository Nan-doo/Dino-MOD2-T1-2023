import random
import pygame

from dino_runner.components.powerups.desdel import Desdel


class DesacelerarManager:
    def __init__(self):
        self.des = []
        self.when_appears = 0

    def generate_desac(self, score):
        if len(self.des) == 0 and self.when_appears == score:
            self.when_appears += random.randint(700, 800)
            self.des.append(Desdel())

    def update(self, game, score):
        self.generate_desac(score)
        for desac in self.des:
            desac.update(game.game_speed, self.des)
            if game.player.dino_rect.colliderect(desac.rect):
                game.game_speed = 20
                self.des.remove(desac)

    def draw(self, screen):
        for desac in self.des:
            desac.draw(screen)

    def reset_des(self):
        self.des = []
        self.when_appears = random.randint(200, 300)