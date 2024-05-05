import random

import keras
import numpy


class Agent:
    def __init__(self, load: bool):
        # env set
        self.state_size = 2
        self.action_size = 3
        self.actions = [0, 1, 2]

        # parameter
        self.discount_factor = 0.99
        self.learning_rate = 0.005
        self.epsilon = 1
        self.epsilon_decay = .999
        self.epsilon_min = 0.01
        self.model = keras.Sequential()
        self.optimizer = keras.optimizers.Adam(learning_rate=self.learning_rate)

        # model setting
        if load:
            self.model = keras.models.load_model('./model/deep_sarsa_model.keras')
        else:
            self.model.add(keras.layers.Dense(30, input_dim=self.state_size, activation='relu'))
            self.model.add(keras.layers.Dense(30, activation='relu'))
            self.model.add(keras.layers.Dense(self.action_size, activation='linear'))
            self.model.summary()
            self.model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate))

    def get_action(self, state: list[float or int]):
        if numpy.random.rand() < self.epsilon:
            return random.choice(self.actions)
        else:
            q = self.model.predict(numpy.float32(state))
            # return max value's index
            return numpy.argmax(q[0])

    def train(self, state, action, reward, next_state, next_action):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # pre-processing
        state = numpy.float32(state)
        next_state = numpy.float32(next_state)

        # train
        current_qtable = self.model.predict(state)[0]
        next_qtable = self.model.predict(next_state)[0]

        current_qtable[action] = reward + self.discount_factor * next_qtable[next_action]
        current_qtable = numpy.reshape(current_qtable, [1, self.action_size])

        self.model.fit(state, current_qtable, epochs=1, verbose=0)

        print('-' * 25)
        print('reward = {}, state : {}'.format(reward, state))
        print('e = {}, q : {}'.format(self.epsilon, list(current_qtable)))
        print('-' * 25)



