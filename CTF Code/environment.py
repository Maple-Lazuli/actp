import numpy as np
import json
import brick_code as bc

with open("actions.json", "r") as file_in:
    action_mapper = json.load(file_in)


class Environment:
    def __init__(self):
        self.board = np.zeros((20, 10))
        self.done = False
        self.reward = 0

    def update(self, raw_response: bytes):
        response = raw_response.decode()

        if response.find("GAME OVER") != -1:
            self.done = True
            self.reward += 1
        else:
            self.board = bc.get_current_board(response)
            self.block, self.offset = bc.get_current_block(response)
            self.chunk = raw_response
            self.reward += 1
            self.done = False
        
    def reset(self):
        self.board = np.zeros((20, 10))
        self.reward = 0

    def board_to_state(self):
        return bc.arr_to_int(self.board)

    def get_state(self):

        return {
            'state': self.board_to_state(),
            'board': self.board,
            'block': self.block,
            'offset': self.offset,
            'reward': self.reward,
            'done': self.done
        }
