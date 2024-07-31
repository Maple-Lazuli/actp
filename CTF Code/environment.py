import numpy as np
from copy import deepcopy
import json

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

def get_blocked_spots(matrix):
    count = 0
    for idx in range(2, matrix.shape[0]):
        row_to_check = matrix[idx]   
        rows_to_compare = matrix[:idx].sum(axis=0)
        
        count += (row_to_check == 0).sum()  - (((row_to_check == 0) & (rows_to_compare == 0))).sum()
        
    return count

def get_current_block(sample):
    current_block = sample.split("----------")[0]
    lines = current_block.split("\n")
    cut = 0
    for idx, val in enumerate(lines):
        if "/" in val:
            cut = idx +1
            break
    lines = lines[cut:]
    lines = [l for l in lines if len(l.strip()) != 0]
    # transpose to remove excess white space
    transpose = []
    for i in range(len(lines[0])):
        temp = ""
        for j in range(len(lines)):
            temp += lines[j][i]
        if temp.strip() != "":
            transpose.append(temp)

    # get X offset
    offset = 10
    for i in range(len(lines)):
        temp = 0
        for j in range(len(lines[i])):
            if lines[i][j] != ' ':
                temp = max(temp, j)
                break
            temp = max(temp, j)
        offset = min(temp, offset)
    
    # detranspose
    depth = len(lines)
    for i in range(depth):
        lines[i] = ""
    for t in range(len(transpose)):
        for l in range(len(transpose[t])):
            lines[l] += transpose[t][l]

    for i in range(len(lines)):
        lines[i] = [0 if l == " " else 1 for l in lines[i]]
        
    return np.array(lines), offset


def is_terminal(board):
    """
    If board is terminal, returns 1 or -1 depending on winner, or 0 if tie
    If board is not terminal, returns None
    """
    for turn in [-1, 1]:
        mask = board == turn
        out = mask.all(0).any() | mask.all(1).any()
        out |= np.diag(mask).all() | np.diag(mask[:, ::-1]).all()

        if out:
            return turn

    if not np.any(board == 0):
        return 0

    return None


class Environment:
    def __init__(self, size=3):
        self.board = np.zeros((size, size))
        self.size = size

    def update(self, new_board):
        self.board = deepcopy(new_board)

    def reset(self):
        self.board = np.zeros((20, 10))

    def board_to_state(self):
        return arr_to_int(self.board)

    def get_state(self):
        return {
            'state': self.board_to_state(),
            'board': self.board,
            'turn': self.turn,
            'reward': 0 if is_terminal(self.board) is None else is_terminal(self.board),
            'done': False if is_terminal(self.board) is None else True
        }

    def is_done(self):
        return False if is_terminal(self.board) is None else True