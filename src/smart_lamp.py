import random
import numpy as np
import os
import tensorflow as tf
import collections
import time
import pandas as pd






########
## Deep Q Network Lamp; in this case will also be some environmental variables built into
## the lamps
########

class DQNLamp:
    def __init__(self):
#        self.model_path = "/Users/ben/Documents/GitRepos/lamps/models/"
        self.memory = collections.deque(maxlen=1000000)
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.996
        self.learning_rate = 0.001
        self.numStateParameters = 4
        self.actionSpace = [0,1,2,3,4]
        self.model = self.create_model() #### This does the actual predictions
        
        
    def create_model(self):
        model = tf.keras.Sequential()
        ## there are 4 parameters in our states: energy,x&y velocity,scentMagnitude
        state_shape = (self.numStateParameters,)
        model.add(tf.keras.layers.Dense(150, input_dim=self.numStateParameters, activation="relu"))
        model.add(tf.keras.layers.Dense(50, activation="relu"))
        model.add(tf.keras.layers.Dense(len(self.actionSpace)))
        model.compile(loss="mean_squared_error", optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return

        ### get a random batch from our memory of states and outcomes
        samples = random.sample(self.memory, batch_size)

        all_states = np.reshape([np.squeeze(x[0]) for x in samples], (batch_size, self.numStateParameters))
        all_actions = np.reshape([x[1] for x in samples], (batch_size, ))
        all_rewards = np.reshape([x[2] for x in samples], (batch_size, ))
        all_new_states = np.reshape([np.squeeze(x[3]) for x in samples], (batch_size, self.numStateParameters))
        all_dones = np.reshape([x[4] for x in samples], (batch_size, ))

        # make predictions of future rewards based on the batch of new states that we obtained
        future_discounted_rewards = np.array(self.model.predict_on_batch(all_new_states))
        
        # figure out which reward is best & pick biggere one
        future_max_reward = np.amax(future_discounted_rewards, axis=1)
        ### add future max reward for each time the game won't be over to our current total reward



        updated_future_discounted_rewards =  all_rewards + self.gamma*future_max_reward*(~all_dones)
        all_targets = np.array(self.model.predict_on_batch(all_states)) # get us predicted rewards
        all_targets[np.arange(len(all_targets)), np.array(all_actions)] = updated_future_discounted_rewards # updated predicted rewards

        ### all  states predicts the Q-value from our network prediction
        ### all values is the Q-value after taking the action
        ### we want to make the Q value from our network prediction match our target
        self.model.train_on_batch(all_states, all_targets)


    def act(self, state):
        # render it more likely for lamp to make best guess action
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min,self.epsilon)
        if np.random.random() < self.epsilon:
            random_action = random.sample(self.actionSpace,1)[0]
            return random_action
        else:            
            state = np.array([state])
            return np.argmax(self.model.predict(state)[0])

    def save_model(self, fn):
        self.model.save(fn)
        

