import random

import pygame

# window setting
window_setting = [900, 600]
window = pygame.display.set_mode(window_setting)


# player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.velocity = 10

        self.rect.center = [25, 25]

    def update(self, action: int):
        match action:
            case 0:
                self.rect.x += self.velocity
            case 1:
                self.rect.x -= self.velocity
            case 2:
                self.rect.y += self.velocity
            case 3:
                self.rect.y -= self.velocity
            case 4:
                pass
            case _:
                raise ValueError(f'Invalid action: {action}')

        if self.rect.right > window_setting[0]:
            self.rect.right = window_setting[0]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > window_setting[1]:
            self.rect.bottom = window_setting[1]
        if self.rect.top < 0:
            self.rect.top = 0


# enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((65, 65))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

        # True means '+' direction and False means opposite
        self.direction = [random.choice([True, False]), random.choice([True, False])]
        self.velocity = [random.choice(range(5, 15)), random.choice(range(5, 15))]

        self.rect.center = [window_setting[0] / 2, window_setting[1] / 2]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]\

        if self.rect.right > window_setting[0]:
            self.rect.right = window_setting[0]
            self.new_direction([False, random.choice([True, False])])
        if self.rect.left < 0:
            self.rect.left = 0
            self.new_direction([True, random.choice([True, False])])
        if self.rect.bottom > window_setting[1]:
            self.rect.bottom = window_setting[1]
            self.new_direction([False, random.choice([True, False])])
        if self.rect.top < 0:
            self.rect.top = 0
            self.new_direction([True, random.choice([True, False])])

    def new_direction(self, direction: [bool, bool]):
        self.velocity = [random.choice(range(5, 15)), random.choice(range(5, 15))]

        if direction[0]:
            pass
        else:
            self.velocity[0] *= -1
        if direction[1]:
            pass
        else:
            self.velocity[1] *= -1


# target class
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((75, 75))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()

        [self.rect.right, self.rect.bottom] = window_setting

    def update(self):
        pass


# update and draw
def uad(action: int):
    window.fill((255, 255, 255))
    window.blit(player.image, player.rect)
    player.update(action)
    window.blit(target.image, target.rect)
    enemy_group.update()
    enemy_group.draw(window)
    pygame.display.update()


def reset():
    player.rect.center = [25, 25]
    enemy_group.empty()
    for _ in range(2):
        # noinspection PyTypeChecker
        enemy_group.add(Enemy())
    target.rect.right, target.rect.bottom = window_setting

    return get_state()


def get_state():
    state = [target.rect.x - player.rect.x, target.rect.y - player.rect.y]
    for enemy in enemy_group:
        state.append(enemy.rect.x - player.rect.x)
        state.append(enemy.rect.y - player.rect.y)
        state.append(enemy.velocity[0])
        state.append(enemy.velocity[1])

    return state


def get_reward():
    reward = 0
    for _ in pygame.sprite.spritecollide(player, enemy_group, False):
        reward += -1
    if player.rect.colliderect(target.rect):
        reward += 10
    return reward - 0.1


def step():
    done = False
    if player.rect.colliderect(target.rect):
        done = True

    return get_state(), get_reward(),done


# entity setting
player = Player()
enemy_group = pygame.sprite.Group()
for _ in range(2):
    # noinspection PyTypeChecker
    enemy_group.add(Enemy())
target = Target()
