import datetime
import json
import os
from math import sqrt
import numpy as np
import random
import shutil
import matplotlib.pyplot as plt
import brick_code as bc

with open("actions.json", "r") as file_in:
    actions = json.load(file_in)

class Agent:

    def __init__(self, random_seed=101011, lr=0.01, epsilon=(0.01, 1.0), num_episodes=10000,
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
        self.random_seed = random_seed
        self.lr = lr
        self.epsilon = epsilon
        self.num_episodes = num_episodes
        self.current_episode = 0
        self.q_table = dict()

        self.past_results = []

        self.episode_memory = []

        np.random.seed(random_seed)

    def get_epsilon(self):
        epsilon = max(self.epsilon[0], min(self.epsilon[1], self.num_episodes / (self.current_episode + 1)))
        return epsilon

    def act(self, board, block, offset):
        epsilon = self.get_epsilon()

        available_moves = bc.get_moves(board, block, offset)

        if np.random.random() < epsilon:
            action = random.choice(available_moves)
        else:
            action = self.perform(board, block, offset)

        return action

    def step(self, state, action, next_state):
        self.episode_memory.append([state, action['block_type'], next_state])

    def update(self, reward):
        # Update q-table
        # might need to update the q-table action space to be the cartesian product of blocks * actions 
        for current_state, action, new_state in self.episode_memory:
            if current_state not in self.q_table:
                self.add_state_to_q(current_state)
            if new_state not in self.q_table:
                self.add_state_to_q(new_state)

            self.q_table[current_state][action] = self.q_table[current_state][action] + self.lr * (
                    reward + max([self.q_table[new_state][k] for k in self.q_table[new_state]]) -
                    self.q_table[current_state][action])
                            
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
                "epsilon": f'{self.epsilon[0]} - {self.epsilon[1]}',
                "q_table": self.q_table
            }, file_out)


    def perform(self, board, block, offset):
        # use q table to find the best move
        # here q table will basically be a dict of dicts
        # get a available moves given the current board
        # return the move with the highest score

        moves = bc.get_moves(board, block, offset)
        # might need to verify whether the state is in the q table or not.
        state_mapping = bc.arr_to_int(board)
        if state_mapping not in self.q_table:
                self.add_state_to_q(state_mapping)
        
        seen_moves = self.q_table[state_mapping]

        best_move= ""
        best_move_score = 0
        for move in moves:
            # moves is currently a list of dicts, need to
            # translate to a seen_moves key in the q table
            q_key = move['op'] + move['block_type']
            if q_key in seen_moves.key():
                if seen_moves[q_key] >= best_move_score:
                    best_move = move
                    best_move_score = seen_moves[q_key] 

        return best_move

    def add_state_to_q(self, state):
        self.q_table[state] = dict()
        for action in actions:
            self.q_table[state][action] = 0