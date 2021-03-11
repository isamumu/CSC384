"""
An AI player for Othello. 
"""

import random
import sys
import time

min_list = dict()
max_list = dict()
betas = dict()
alphas = dict()

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    score = get_score(board)
    # 1 for dark; 2 for light
    # get_score returns tuple (dark disks, light disks)
    # this function should return the number of player's disks minus number of disks of the opponent
    if color == 1:
        return score[0] - score[1]
    return score[1] - score[0] #change this!

# return count of corner pieces
def isCorner(board, color):
    dim = len(board) - 1
    score = 0
    if board[0][dim] == color:
        score += 10
    
    if board[0][0] == color:
        score += 10
    
    if board[dim][0] == color:
        score += 10
    
    if board[dim][dim] == color:
        score += 10
    
    if board[1][0] == color or board[1][1] == color or board[0][1] == color:
        score -= 5
    
    if board[dim-1][0] == color or board[dim-1][1] == color or board[dim][1] == color:
        score -= 5

    if board[0][dim-1] == color or board[1][dim-1] == color or board[1][dim] == color:
        score -= 5

    if board[dim-1][dim] == color or board[dim-1][dim-1] == color or board[dim][dim-1] == color:
        score -= 5

    return score

# return heuristic count of immune pieces (edges aren't always immune, but have the highest chances of becoming immune)
def isImmune(board, color):
    # generally, the edges are immune spots as long as they are 2 positions away from the corner
    score = 0

    for i in range(2, len(board) - 2):
        if board[i][0] == color: 
            score += 1
        if board[i][len(board) - 1] == color:
            score += 1
        if board[0][i] == color:
            score += 1
        if board[len(board) - 1][i] == color:
            score += 1
    return score

def mobilityCount(board, color):
    count = len(get_possible_moves(board, color))
    return count

# Better heuristic value of board
def compute_heuristic(board, color): 
    #IMPLEMENT
    # the custom heuristic depends on the following heuristics:
    # -> if pieces are in the corners (reward)
    # -> parity count (reward if positive)
    # -> mobility scaled (number of possible moves left)
    # -> immunity (rewarding pieces that seldom get altered)
    return compute_utility(board, color) + isCorner(board, color) + (mobilityCount(board, color) / 2) + isImmune(board, color) #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0): #returns the lowest possible utility?
    #IMPLEMENT (and replace the line below)

    # modify the opponent's color here since we fix the colour value in the input
    opponent = color
    if color == 1:
        opponent = 2
    if color == 2:
        opponent = 1

    # if caching, find the value inside the global dictionary if it exists
    if caching:
        if (board, opponent) in min_list:
            return min_list[(board, opponent)]

    movesLeft = get_possible_moves(board, opponent)

    # if no moves left i.e. terminal node
    # if there are no possible moves or we reach the depth limit
    if movesLeft == [] or limit == 0:
        return (None, compute_utility(board,color))
        # return (None, compute_heuristic(board,color))

    # initialize the initial value to be infinite
    minVal = float('inf')
    minMove = movesLeft[0] # initialize the minimum move to be the first possible move left

    # if moves are still left
    for move in movesLeft:
        '''
        The logic: 
        --> compute the next state and compute the max node for every possible move
        --> logically, min will choose the move in which max chooses the minimum option
        --> once we found a maxVal less than the minval, update the minVal value
        '''
        # obtain the next board
        next_board = play_move(board, opponent, move[0], move[1])
        # find the value selected by the max node
        maxVal = minimax_max_node(next_board, color, limit-1, caching)[1]

        # update if necessary
        if maxVal < minVal:
            minVal = maxVal
            minMove = move
    
    # if caching is involved, store the move pair into the dictionary
    if caching:
        min_list[(board, opponent)] = (minMove, minVal)

    return (minMove,minVal)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT (and replace the line below)
    
    # if caching, find the value inside the global dictionary if it exists
    if caching:
        if (board, color) in max_list:
            return max_list[(board, color)]

    movesLeft = get_possible_moves(board, color)
    
    # if no moves left i.e. terminal node
    # if there are no possible moves or we reach the depth limit
    if movesLeft == [] or limit == 0:
        return (None, compute_utility(board,color))
        # return (None, compute_heuristic(board,color))

    # initialize the maximum value to be negative infinity
    maxVal = float('-inf')
    maxMove = movesLeft[0] # initialize the minimum move to be the first possible move left
    
    # if moves are still left
    for move in movesLeft:
        '''
        The logic: 
        --> compute the next state and compute the min node for every possible move
        --> logically, max will choose the move in which min chooses the maximum option
        --> once we found a minVal greater than the maxval, update the maxVal value
        '''
        # obtain the next board
        next_board = play_move(board, color, move[0], move[1])
        # obtain the value selected by the min node
        minVal = minimax_min_node(next_board, color, limit-1, caching)[1]
        if minVal > maxVal:
            maxVal = minVal
            maxMove = move
    
    # store the value inside the global dictionary
    if caching:
        max_list[(board, color)] = (maxMove, maxVal)

    return (maxMove, maxVal)

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT (and replace the line below)
    
    
    return minimax_max_node(board, color, limit, caching)[0] #change this!

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)
    
    # adjust the opponents color as necessary
    opponent = color
    if color == 1:
        opponent = 2
    if color == 2:
        opponent = 1

    # if caching is involved use the contained value if it exists
    if caching:
        if(board, opponent) in betas:
            return betas[(board, opponent)]

    # obtain the moves left for the opponent's color
    movesLeft = get_possible_moves(board, opponent)

    # create a list of boards which will be used for ordering 
    boards = []
    for move in movesLeft:
        newboard = play_move(board, opponent, move[0], move[1])
        boards.append(newboard)
    
    # if we want to order, sort it in descending order based on the calculated utility function
    if ordering:
        boards.sort(key=lambda board: compute_utility(board, color), reverse=True)

    # if no moves left i.e. terminal node
    # if there are no possible moves or we reach the depth limit
    if movesLeft == [] or limit == 0:
        if caching:
            betas[(board, opponent)] = (None, compute_utility(board,color))
            # betas[(board, opponent)] = (None, compute_heuristic(board,color))
        return (None, compute_utility(board,color))
        # return (None, compute_heuristic(board,color))
    
    minVal = float('inf')
    minMove = movesLeft[0] # initialize the minimum move to be the first possible move left
    
    # if we want ordering use the ordered list of states
    # otherwise, just iterate through the remaining moves
    if ordering: 
        for nextBoard in boards:
            # nextBoard = play_move(board, opponent, move[0], move[1])
            utilVal = alphabeta_max_node(nextBoard, color, alpha, beta, limit-1, caching, ordering)

            if utilVal[1] < minVal:
                minMove = move
                minVal = utilVal[1]        

            beta = min(beta, minVal)
            # pruning criteria
            if beta <= alpha:
                break
    else: 
        for move in movesLeft:
            nextBoard = play_move(board, opponent, move[0], move[1])
            utilVal = alphabeta_max_node(nextBoard, color, alpha, beta, limit-1, caching, ordering)

            if utilVal[1] < minVal:
                minMove = move
                minVal = utilVal[1]        

            beta = min(beta, minVal)
            if beta <= alpha:
                break
    
    if caching:
        betas[(board, opponent)] = (minMove, minVal)

    return (minMove, minVal) #change this!

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)
    # if no moves left i.e. terminal node
    # if there are no possible moves or we reach the depth limit

    if caching:
        if(board, color) in betas:
            return alphas[(board, color)]

    movesLeft = get_possible_moves(board, color)

    # create a list of boards which will be used for ordering 
    boards = []
    for move in movesLeft:
        newboard = play_move(board, color, move[0], move[1])
        boards.append(newboard)
    
    if ordering:
        boards.sort(key=lambda board: compute_utility(board, color), reverse=True)

    if movesLeft == [] or limit == 0:
        if caching:
            alphas[(board, color)] = (None, compute_utility(board,color))
            # alphas[(board, color)] = (None, compute_heuristic(board,color))
        return (None, compute_utility(board,color))
        # return (None, compute_heuristic(board,color))
    
    maxVal = float('-inf')
    maxMove = movesLeft[0] # initialize the minimum move to be the first possible move left

    # if we want ordering use the ordered list of states
    # otherwise, just iterate through the remaining moves
    if ordering:
        for nextBoard in boards:
            # nextBoard = play_move(board, color, move[0], move[1])
            utilVal = alphabeta_min_node(nextBoard, color, alpha, beta, limit-1, caching, ordering)

            if utilVal[1] > maxVal:
                maxMove = move
                maxVal = utilVal[1]     

            alpha = max(alpha, maxVal)
            if beta <= alpha:
                break
    else:
        for move in movesLeft:
            nextBoard = play_move(board, color, move[0], move[1])
            utilVal = alphabeta_min_node(nextBoard, color, alpha, beta, limit-1, caching, ordering)

            if utilVal[1] > maxVal:
                maxMove = move
                maxVal = utilVal[1]     

            alpha = max(alpha, maxVal)
            if beta <= alpha:
                break
        
    if caching:
        alphas[(board, color)] = (maxMove, maxVal)

    return (maxMove, maxVal) #change this!

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT (and replace the line below)
    # since the min and max functions are recursive, all  we need to do is call the max function! 
    return alphabeta_max_node(board, color, float("-inf"), float("inf"), limit, caching = 0, ordering = 0)[0] #change this!

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
