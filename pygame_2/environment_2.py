import random

import pygame
from pygame_2.environment_1 import Player, Target

# window setting
window_setting = [900, 600]
window = pygame.display.set_mode(window_setting)

# entity setting
player = Player()
target = Target()

state_size = 2


# update and draw
def uad(action: int):
    window.fill((255, 255, 255))
    window.blit(player.image, player.rect)
    player.update(action)
    window.blit(target.image, target.rect)
    pygame.display.update()


def reset():
    player.rect.center = [25, 25]
    target.rect.right, target.rect.bottom = window_setting

    return get_state()


def get_state():
    state = [target.rect.x - player.rect.x, target.rect.y - player.rect.y]

    return state


def get_reward():
    reward = 0
    if player.rect.colliderect(target.rect):
        reward += 10
    return reward


def step():
    a = 0
    done = False
    if player.rect.colliderect(target.rect):
        done = True

    return get_state(), get_reward(), done
