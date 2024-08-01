import numpy as np
from copy import deepcopy

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

def get_current_board(sample):
    current_board = sample.split("----------")[2]
    lines = current_board.split("\n")[1:-1]
    for i in range(len(lines)):
        lines[i] = [0 if l == " " else 1 for l in lines[i]]
    return np.array(lines)


def get_candidates(board, block, offset):
    candidates = []

    for op in generate_operations():
        offset_x = offset
        
        bo = deepcopy(board)
        bl = deepcopy(block)
        
        offset_x += op.count('r')
        offset_x -= op.count('l')
        
        if 'q' in op:
            bl = np.rot90(bl)
            bl = np.rot90(bl)
            bl = np.rot90(bl)
        elif 'cc' in op:
            bl = np.rot90(bl)
            bl = np.rot90(bl)
        elif 'c' in op:
            bl = np.rot90(bl)
        if offset_x < 0:
            continue
        if offset_x > 10:
            continue
        try:
            offset_y = 0
            for _ in range(min(18,20-bl.shape[0])):
                sub = bo[offset_y:(bl.shape[0]+offset_y), offset_x:(bl.shape[1]+offset_x)]
                if np.any((sub + bl) == 2):
                    break
                offset_y +=1
            bo[offset_y:(bl.shape[0]+offset_y), offset_x:(bl.shape[1]+offset_x)] = bl
        except:
            pass
        candidates.append({'op':op, 'matrix':bo})
    return candidates


def generate_operations():
    operations = ['l','q','c','r', 'cc']
    for l in 'lr':
        for i in range(2,9):
            operations.append(l*i)
            operations.append(l*i+'q')
            operations.append(l*i+'c')
            operations.append(l*i+'cc')
    return operations


# First Attempt at making a bot decide a move.
def get_best_candidate_old(candidates):
    len_score = 1000
    most_lines = 0
    least_blocks = 200
    for candidate in candidates:
        m = candidate['matrix']
        
        l_score = (m.sum(axis = 1) != 0).sum()
        score = np.exp((m.sum(axis = 1) * np.linspace(.1,1,num=m.shape[0]))).sum()
        len_score = min(len_score, l_score)
        candidate['len_score'] = l_score
        candidate['score'] = score
        blocked_blocks = get_blocked_spots(m)
        least_blocks = min(least_blocks, blocked_blocks)
        candidate['blocked_blocks'] = blocked_blocks
        lines = np.any(m.sum(axis = 1) == m.shape[1]).sum()
        most_lines = max(most_lines, lines)
        candidate['lines'] = lines
        
    if most_lines != 0:
        for candidate in candidates:
            if candidate['lines'] == most_lines:
                return candidate
    
    if least_blocks != 200:
        len_score = 1000
        temp_cans = []
        for candidate in candidates:
            if candidate['blocked_blocks'] == least_blocks:
                if candidate['len_score'] <= len_score:
                    len_score = candidate['len_score']


        for candidate in candidates:
            if candidate['blocked_blocks'] == least_blocks:
                if candidate['len_score'] == len_score:
                    temp_cans.append(candidate)

        best_score = 0
        for candidate in temp_cans:
            if candidate['score'] >= best_score:
                can = candidate
                best_score = candidate['score']
        
        if can is not None:
            return can
        


    best_score = 0
    can = None
    for candidate in candidates:
        if candidate['len_score'] == len_score:
            if candidate['score'] >= best_score:
                can = candidate
                best_score = candidate['score']
    return can
    
# Second attempt at deciding a best candidate
def get_best_candidate(candidates):

    most_lines = 0
    for candidate in candidates:
        m = candidate['matrix']
        
        l_score = (m.sum(axis = 1) != 0).sum()
        candidate['len_score'] = l_score
        
        blocked_blocks = get_blocked_spots(m)
        candidate['blocked_blocks'] = blocked_blocks
        candidate['score'] =  (m.sum(axis = 1) * np.log(np.linspace(1,20, num=m.shape[0]))).sum() - (np.log(candidate['blocked_blocks']+1)*2)
       # candidate['score'] =  (m.sum(axis = 1) * np.exp(np.linspace(1,10, num=m.shape[0]))).sum() - (np.exp(candidate['blocked_blocks']))
       # candidate['score'] =  np.exp((m.sum(axis = 1) == 0).sum()) - (np.exp(candidate['blocked_blocks']))
        lines = np.any(m.sum(axis = 1) == m.shape[1]).sum()
        most_lines = max(most_lines, lines)
        candidate['lines'] = lines
        
    if most_lines != 0:
        for candidate in candidates:
            if candidate['lines'] == most_lines:
                return candidate
    
        
    best_score = candidates[0]['score']
    can = None
    for candidate in candidates:
        if candidate['score'] >= best_score:
            can = candidate
            best_score = candidate['score']
                    
    return can
    

if __name__ == "__main__":

    sample = """
1/15
   OOOO   
----------
0123456789
----------
          
          
          
          
          
          
          
          
          
          
          
      QQ  
  B  QQ   
OBBB O    
O X% O    
OXX% O8888
OX %%O8888
OOOO % % B
   Q % %BB
  0 Q OOOO
----------
0123456789
----------

"""

    block, offset = get_current_block(sample)
    board = get_current_board(sample)
    candidates = get_candidates(board, block, offset)
    c = get_best_candidate(candidates)
    print(c)