import random
import math

window_size = [1200, 900]


class Player:
    def __init__(self, size: int, vel: int):
        self.center = [0, 0]
        self.size = size
        self.vel = vel

        self.center[0] = window_size[0] / 2
        self.center[1] = window_size[1] - self.size / 2

    def move(self, action: int):
        match action:
            case 0:
                pass
            case 1:
                self.center[0] += self.vel
            case 2:
                self.center[0] -= self.vel

        # 양 옆 이동 제한
        if self.center[0] + self.size / 2 > window_size[0]:
            self.center[0] = window_size[0] - self.size / 2
        if self.center[0] - self.size / 2 < 0:
            self.center[0] = self.size / 2


class Target:
    def __init__(self, size: int, vel: int):
        self.center = [0, 0]
        self.size = size
        self.vel = vel

        self.center[0] = random.choice(range(int(self.size / 2), int(window_size[0] - self.size / 2)))
        self.center[1] = self.size / 2

    def move(self):
        self.center[1] += self.vel

        if self.center[1] - self.size / 2 > window_size[1]:
            self.__init__(self.size, self.vel)


def collide(p: Player, t: Target):
    if math.fabs(p.center[0] - t.center[0]) < p.size + t.size:
        if math.fabs(p.center[1] - t.center[1]) < p.size + t.size:
            return True

    return False


# entity setting
player = Player(50, 10)
target = Target(50, 10)


def get_state():
    """return list: [player center x: [0, 1], target center x: [0, 1], target center y: [0, 1]]"""
    return [
        player.center[0] / 1200,
        player.center[0] / 1200,
        target.center[1] / 900]


def get_reward():
    if collide(player, target):
        return 100

    return 0
