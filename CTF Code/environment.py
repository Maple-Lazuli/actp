import numpy as np
import json
import brick_code as bc

with open("actions.json", "r") as file_in:
    action_mapper = json.load(file_in)

def arr_to_str(b):
    big_s = ""
    for i in range(b.shape[0]):
        s = ""
        for j in range(b.shape[1]):
            s += str(b[i][j])
        big_s += "\n" + s
    return big_s.strip()

def arr_to_int(board):
    return int("".join([str(b) for b in board.flatten()]),2)

def get_lines(raw_response:bytes):
    return int(raw_response.split()[-2].decode().split("/")[0])


class Environment:
    def __init__(self):
        self.board = np.zeros((20, 10))
        self.done = False
        self.reward = 0

    def update(self, raw_response: bytes):
        self.board = bc.get_current_board(raw_response.decode())
        self.reward += 1
        self.is_done(raw_response)
        
    def reset(self):
        self.board = np.zeros((20, 10))

    def board_to_state(self):
        return arr_to_int(self.board)

    def get_state(self):
        return {
            'state': self.board_to_state(),
            'board': self.board,
            'reward': self.reward,
            'done': self.done
        }

    def is_done(self, raw_respnse):
        if raw_respnse.decode().find("GAME OVER") != -1:
            self.done = True
        self.done = False