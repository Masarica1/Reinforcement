import copy
import random
import numpy as np
import matplotlib.pylab as pylab
from example.environment import Env
from keras import layers
import keras

EPISODES = 1000


# this is DeepSARSA Agent for the GridWorld
# Utilize Neural Network as q function approximate
class DeepSARSAgent:
    def __init__(self, state_size: int):
        self.load_model = True
        # actions which agent can do
        self.action_space = [0, 1, 2, 3, 4]
        # get size of state and action
        self.action_size = len(self.action_space)
        self.state_size = state_size
        self.discount_factor = 0.99
        self.learning_rate = 0.001

        self.epsilon = 1.  # exploration
        self.epsilon_decay = .9999
        self.epsilon_min = 0.01
        self.model = self.build_model()

        if self.load_model:
            self.epsilon = 0.05
            self.model.load_weights("./model/deep_sarsa.weights.h5")

    # approximate Q function using Neural Network
    # state is input and Q Value of each action is output of network
    def build_model(self):
        model = keras.models.Sequential()
        model.add(layers.Dense(30, input_dim=self.state_size, activation='relu'))
        model.add(layers.Dense(30, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.summary()
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    # get action from model using epsilon-greedy policy
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            # The agent acts randomly
            return random.randrange(self.action_size)
        else:
            # Predict the reward value based on the given state
            state = np.float32(state)
            q_values = self.model.predict(state)
            return np.argmax(q_values[0])

    def train_model(self, state, action, reward, next_state, next_action, done):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        state = np.float32(state)
        next_state = np.float32(next_state)
        target = self.model.predict(state)[0]
        # like Q Learning, get maximum Q value at s'
        # But from target model
        if done:
            target[action] = reward
        else:
            target[action] = (reward + self.discount_factor *
                              self.model.predict(next_state)[0][next_action])

        target = np.reshape(target, [1, 5])
        # make minibatch which includes target q value and predicted q value
        # and do the model fit!
        self.model.fit(state, target, epochs=1, verbose=0)


if __name__ == "__main__":
    env = Env()
    agent = DeepSARSAgent(15)

    global_step = 0
    scores, episodes = [], []

    for e in range(EPISODES):
        done = False
        score = 0
        state = env.reset()
        state = np.reshape(state, [1, 15])

        while not done:
            # fresh env
            global_step += 1

            # get action for the current state and go one step in environment
            action = agent.get_action(state)
            next_state, reward, done = env.step(action)
            next_state = np.reshape(next_state, [1, 15])
            next_action = agent.get_action(next_state)
            agent.train_model(state, action, reward, next_state, next_action,
                              done)
            state = next_state
            # every time step we do training
            score += reward

            state = copy.deepcopy(next_state)

            if done:
                scores.append(score)
                episodes.append(e)
                pylab.plot(episodes, scores, 'b')
                pylab.savefig("./save_graph/deep_sarsa_.png")
                print("episode:", e, "  score:", score, "global_step",
                      global_step, "  epsilon:", agent.epsilon)

        if e % 100 == 0:
            agent.model.save_weights("./save_model/deep_sarsa.weights.h5")
