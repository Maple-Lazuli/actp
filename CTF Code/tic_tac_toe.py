import socket
import time

def play():
    used = []
    while True:
        time.sleep(.02)
        current_board = s.recv(2048).decode('utf-8')
        print(current_board)
        if current_board.find("You won!") != -1:
            s.send(b'4')
            continue
        if current_board.find("Can't make that move") != -1:
            while True:
                val = str(random.randint(0,8))
                if val not in used:
                    break
            used.append(val)
            s.send(val.encode())
            continue
        if current_board.find("+---+---+---+") == -1:
            continue
        current_board = current_board.split("\n")
        used = []
        grid = [[],[],[]]
        grid[0] = current_board[-7].split("|")
        grid[1] = current_board[-5].split("|")
        grid[2] = current_board[-3].split("|")
        for _ in range(0,3):
            grid[_] = [l for l in grid[_] if len(l) > 0]
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j].find("X") != -1:
                    grid[i][j] = 1
                elif grid[i][j].find("O") != -1:
                    grid[i][j] = -1
                else:
                    grid[i][j] = 0
        print(grid)
        play = search_for_play(grid)
        print("Play: ", play)
        s.send(str(play).encode())
        

def search_for_play(grid):
    possibilities = []
    # horiziontal
    for i in range(3):
        indices = []
        score = 0
        for j in range(3):
            indices.append((i,j))
            score += grid[i][j]
        possibilities.append({'positions':indices, 'score':score})
    # vertical 
    for i in range(3):
            indices = []
            score = 0
            for j in range(3):
                indices.append((j,i))
                score += grid[j][i]
            possibilities.append({'positions':indices, 'score':score})
    # diagonal
    indices=[(0,0),(1,1),(2,2)]
    score = grid[0][0] + grid[1][1] + grid[2][2]
    possibilities.append({'positions':indices, 'score':score})

    indices=[(0,2),(1,1),(2,0)]
    score = grid[0][2] + grid[1][1] + grid[2][0]
    possibilities.append({'positions':indices, 'score':score})

    for possibility in possibilities:
        if possibility['score'] == 2:
            return get_valid_move(possibility,grid)
        if possibility['score'] == -2:
            return get_valid_move(possibility,grid)
            
    for possibility in possibilities:
        if possibility['score'] == 1:
            return get_valid_move(possibility,grid)
        

def get_valid_move(possibility, grid):
    score =  possibility['score']
    plays = possibility['positions']
    if grid[1][1] == 0:
        return 4
    if (score == 2) or (score == -2):
        for play in plays:
            i, j = play
            if grid[i][j] == 0:
                return map_index_to_pos(play)
    if (score == 1):
        for play in plays:
            i, j = play
            if grid[i][j] == 0:
                if is_corner(i,j):
                    return map_index_to_pos(play)
        for play in plays:
            i, j = play
            if grid[i][j] == 0:
                return map_index_to_pos(play)
    if (score == 0):
        for play in plays:
            i, j = play
            if grid[i][j] == 0:
                return map_index_to_pos(play)
    if (score == -1):
        for play in plays:
            i, j = play
            if grid[i][j] == 0:
                return map_index_to_pos(play)
   
def map_index_to_pos(play):
    map_grid = [[1,1,1],[1,1,1],[1,1,1]]
    idx = 0
    for i in range(3):
        for j in range(3):
            map_grid[i][j] = idx
            idx +=1
    i,j = play
    return map_grid[i][j]


def is_corner(i,j):
    if (i == 0) and (j == 0):
        return True
    if (i == 0) and (j == 2):
        return True
    if (i == 2) and (j == 0):
        return True
    if (i == 2) and (j == 2):
        return True
    return False

if __name__ == "__main__":
    play()