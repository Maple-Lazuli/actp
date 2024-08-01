import datetime
import json
import os
from math import sqrt
import numpy as np
import random
import shutil
import matplotlib.pyplot as plt


class Agent:

    def __init__(self, state_size, action_size, random_seed=101011, lr=0.01, epsilon=(0.01, 1.0), num_episodes=10000,
                 name="Agent"):
        """
        Instantiate the Agent Class

        :param state_size: Size of the state space
        :param action_size: Size of the action space
        :param random_seed: Seed for exploration
        :param lr: The learning rate
        :param epsilon: The exploration exploitation balancing.
        """
        self.name = name
        self.state_size = state_size
        self.action_size = action_size
        self.action_size_base = int(sqrt(action_size))
        self.random_seed = random_seed
        self.lr = lr
        self.epsilon = epsilon
        self.num_episodes = num_episodes
        self.current_episode = 0
        self.q_table = np.zeros((state_size ** action_size, action_size))

        self.past_results = []

        self.episode_memory = []

        np.random.seed(random_seed)

    def get_epsilon(self):
        epsilon = max(self.epsilon[0], min(self.epsilon[1], self.num_episodes / (self.current_episode + 1)))
        return epsilon

    def act(self, board):
        epsilon = self.get_epsilon()

        available_moves = get_available_moves(board)

        if np.random.random() < epsilon:
            action = random.choice(available_moves)
        else:
            action = self.perform(board)

        return action

    def step(self, state, action, next_state):
        self.episode_memory.append([state, action, next_state])

    def update(self, reward):
        # Update q-table
        for current_state, action, new_state in self.episode_memory:
            self.q_table[current_state, action] = self.q_table[current_state, action] + self.lr * (
                    reward + max(self.q_table[new_state]) - self.q_table[current_state, action])

        self.episode_memory = []
        self.current_episode += 1
        self.metrics(reward)

    def metrics(self, reward):
        self.past_results.append(reward)


    def save(self, save_dir="./data/"):

        save_dir = os.path.join(save_dir, f'{self.name}/')

        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)
        os.makedirs(save_dir)

        with open(os.path.join(save_dir, 'training.json'), "w") as file_out:
            json.dump({
                "name": self.name,
                "time": str(datetime.datetime.now()),
                "lr": self.lr,
                "epsilon": f'{self.epsilon[0]} - {self.epsilon[1]}'
            }, file_out)


    def perform(self, board):
        # use q table to find the best move
        # here q table will basically be a dict of dicts
        # get a available moves given the current board
        # return the move with the highest score

        return action