import copy

import matplotlib.pyplot as plt
import numpy as np

from environment_2 import *
from example.deep_sarsa_agent import DeepSARSAgent

pygame.init()
clock = pygame.time.Clock()
event_1 = pygame.USEREVENT + 1
pygame.time.set_timer(event_1, 250)

# agent setting
agent = DeepSARSAgent(state_size)

# setting
EPISODES = 1000
global_step = 0
scores, episodes = [], []

# loop
for e in range(EPISODES):

    done = False
    score = 0
    state = reset()
    state = np.reshape(state, [1, state_size])
    reward = 0
    action = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == event_1:
                # action and train
                next_state, reward, done = step()
                next_state = np.reshape(next_state, [1, state_size])
                next_action = agent.get_action(next_state)

                agent.train_model(state, action, reward, next_state, next_action, done)

                state = copy.deepcopy(next_state)
                action = next_action

        uad(action)
        clock.tick(120)
        score += 1

        if done:
            scores.append(score)
            episodes.append(e)
            plt.plot(episodes, scores, 'b')
            print("episode:", e, "  score:", score, "global_step",
                  global_step, "  epsilon:", agent.epsilon)

    if e % 50 == 0:
        agent.model.save_weights("./model/deep_sarsa.weights.h5")
        plt.show()

pygame.quit()
