import numpy
import pygame
import random


class Player(pygame_1.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame_1.Surface((75, 75))
        self.rect = self.image.get_rect()
        self.vel = 10

        self.image.fill((255, 0, 0))

        self.rect.bottom = window_h
        self.rect.centerx = window_w / 2

    def update(self, direction: int):
        if direction == 0:
            self.rect.x += self.vel
        elif direction == 1:
            self.rect.x -= self.vel
        elif direction == 2:
            pass
        else:
            raise ValueError

        if self.rect.right > window_w:
            self.rect.right = window_w
        if self.rect.left < 0:
            self.rect.left = 0


class Enemy(pygame_1.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame_1.Surface((75, 75))
        self.rect = self.image.get_rect()
        self.vel = 10

        self.image.fill((0, 255, 255))

        self.rect.top = 0
        self.rect.centerx = random.choice(range(0, window_h, 10))

    def update(self):
        self.rect.move_ip(0, self.vel)

        if self.rect.top > window_h:
            self.__init__()


# window setting
window_w = 1280
window_h = 900
window = pygame_1.display.set_mode((window_w, window_h))

# entity setting
player = Player()
enemy = Enemy()


# function
def get_state():
    return numpy.reshape([player.rect.centerx / 1200, enemy.rect.centerx / 1200], [1, 2])


def get_reward():
    reward = 0
    if player.rect.colliderect(enemy.rect):
        reward += 100
    return reward
