import copy

import pygame

from environment import *
from agent import Agent

# agent set
agent = Agent(False)

pre_state = get_state()
pre_action = agent.get_action(pre_state)
reward = 0

# time setting
clock = pygame.time.Clock()
event_1 = pygame.USEREVENT + 1
pygame.time.set_timer(event_1, 250)

# loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == event_1:
            state = get_state()
            action = agent.get_action(state)

            agent.train(pre_state, pre_action, reward, state, action)

            pre_state, pre_action = copy.deepcopy(state), action
            reward = 0

    # drawing
    window.fill((255, 255, 255))
    player.update(pre_action)
    window.blit(player.image, player.rect)
    enemy.update()
    window.blit(enemy.image, enemy.rect)

    reward += get_reward()

    clock.tick(120)
    pygame.display.update()
pygame.quit()

agent.model.save('./model/deep_sarsa_model.keras')
