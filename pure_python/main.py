import random

import matplotlib.pyplot as plt

import entity
from agent import Agent

agent = Agent()

pre_state = entity.get_state()
pre_action = agent.get_action(pre_state)
reward = 0

time = 0
record = [0]

running = True
while running:
    time += 1

    entity.player.move(pre_action)
    entity.target.move()

    reward += entity.get_reward()
    record[-1] += entity.get_reward()

    state = entity.get_state()
    if reward > 0:
        action = agent.get_action(state)

        agent.train(pre_state, pre_action, reward, state, action)

        pre_state, pre_action = state.copy(), action

        reward = 0
    else:
        if random.random() < 0.04:
            action = agent.get_action(state)

            agent.train(pre_state, pre_action, reward, state, action)

            pre_state, pre_action = state.copy(), action
            reward = 0

    if agent.epsilon < 0.02:
        break

    if time > 1500:
        record.append(0)
        time = 0

agent.model.save('./model/deep_sarsa_model2.keras')

domain = range(len(record))
plt.plot(domain, record)
plt.show()
