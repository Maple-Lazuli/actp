import datetime
import json
import os
from math import sqrt
import numpy as np
import random
import shutil
import matplotlib.pyplot as plt


def get_available_moves(board):
    available_moves = np.argwhere(board == 0).tolist()
    return available_moves


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
        self.win_probs = []
        self.draw_probs = []
        self.sum_q_table = []

        self.episode_memory = []

        np.random.seed(random_seed)

    def get_epsilon(self):
        epsilon = max(self.epsilon[0], min(self.epsilon[1], self.num_episodes / (self.current_episode + 1)))

        return epsilon

    def act(self, board, current_state, turn):
        epsilon = self.get_epsilon()

        available_moves = get_available_moves(board)
        if np.random.random() < epsilon:
            action_square = tuple(random.choice(available_moves))
            action = self.action_size_base * action_square[0] + action_square[1]
        else:
            actions = self.q_table[current_state] * turn
            for action in np.argsort(actions)[::-1]:
                action_square = [action // self.action_size_base, action % self.action_size_base]
                if action_square in available_moves:
                    action_square = tuple(action_square)
                    break

        return action, action_square

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

        try:
            averaging_distance = 1000
            draw_freq, win_freq = np.unique(np.abs(self.past_results[-averaging_distance:]), return_counts=True)[1]
            draw_prob = draw_freq / averaging_distance * 100
            win_prob = win_freq / averaging_distance * 100

            self.draw_probs.append(draw_prob)
            self.win_probs.append(win_prob)
        except:
            # If there hasn't been at least one tie and one win, the above code block will raise an exception.
            self.draw_probs.append(None)
            self.win_probs.append(None)
        self.sum_q_table.append(np.abs(self.q_table).sum())

    def print_metrics(self):
        print("Episode: {}, Epsilon: {:.3f}, Win Probability: {:.3f}, Draw Probability: {:.3f}, Q Sum: {:.3f}".format(
            self.current_episode + 1, self.get_epsilon(), self.win_probs[-1], self.draw_probs[-1],
            self.sum_q_table[-1]))

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

        np.save(os.path.join(save_dir, "q_table.npy"), self.q_table)
        np.save(os.path.join(save_dir, "draw_probs.npy"), np.array(self.draw_probs), allow_pickle=True)
        np.save(os.path.join(save_dir, "win_probs.npy"), np.array(self.win_probs), allow_pickle=True)
        np.save(os.path.join(save_dir, "sum-q.npy"), np.array(self.sum_q_table))

        fig = plt.figure(figsize=(15, 6))
        plt.subplot(1, 2, 1)
        plt.plot(self.draw_probs, label="Draw Probability")
        plt.plot(self.win_probs, label="Win Probability")
        plt.xlim(0, len(self.draw_probs) - 1)
        plt.ylim(0, 100)
        plt.xlabel("Episode")
        plt.ylabel("Probability (%)")
        plt.legend()
        plt.subplot(1, 2, 2)
        plt.plot(self.sum_q_table)
        plt.xlim(0, len(self.sum_q_table) - 1)
        plt.ylim(0, )
        plt.xlabel("Episode")
        plt.ylabel("$\sigma_(s, a) |Q(s, a)|$")
        fig.savefig(os.path.join(save_dir, "performance.png"), dpi=fig.dpi)

    def load(self, save_dir='./data/'):
        save_dir = os.path.join(save_dir, f'{self.name}/')
        self.q_table = np.load(os.path.join(save_dir, "q_table.npy"))

    def perform(self, board, current_state, turn):
        available_moves = get_available_moves(board)
        actions = self.q_table[current_state] * turn
        for action in np.argsort(actions)[::-1]:
            action_square = [action // self.action_size_base, action % self.action_size_base]
            if action_square in available_moves:
                action_square = tuple(action_square)
                break

        return action, action_square