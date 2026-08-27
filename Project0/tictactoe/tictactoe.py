"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0

    for i in range(0, 3):
        for j in range(0,3):
            if board[i][j] == X:
                x = x + 1
            elif board[i][j] == O:
                o = o + 1

    # if x == 5:
    #     return None

    if x == 0 or (x == o):
        return X

    if x > o:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_available = set()

    for i in range(0, 3):
        for j in range(0,3):
            if board[i][j] == EMPTY:
                actions_available.add((i, j))
    return actions_available


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    actions_available = actions(board)
    if not action in actions_available:
        raise NameError("Action not Available")
    
    board_copy = copy.deepcopy(board)

    current_player = player(board)
    board_copy[action[0]][action[1]] = current_player

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if ["X","X","X"] in board:
        return X
        
    if ["O","O","O"] in board:
        return O

    for i in range(0, 3):
        if board[0][i] == board[1][i] == board[2][i] != None:
            if board[0][i] == X:
                return X
            else:
                return O

    if board[0][0] == board[1][1] == board[2][2] != None:
        if board[0][0] == X:
            return X
        else:
            return O

    if board[0][2] == board[1][1] == board[2][0] != None:
        if board[0][2] == X:
            return X
        else:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for i in range(0, 3):
        if EMPTY in board[i]:
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
        
    if winner_player == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    available_actions = actions(board)
    best_action = None
    best_value = -math.inf if player(board) == X else math.inf

    beta = math.inf 
    alpha = -math.inf

    if player(board) == X:

        for action in available_actions:
            value = min_value(alpha, beta, result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
            
    if player(board) == O:

        for action in available_actions:
            value = max_value(alpha, beta, result(board, action))
            if value < best_value:
                best_value = value
                best_action = action

    return best_action


def max_value(alpha, beta, board):
    if terminal(board):
        return utility(board)

    available_actions = actions(board)
    v = -math.inf

    for action in available_actions:
        v = max(v, min_value(alpha, beta, result(board, action)))
        alpha = max(alpha, v)

        if alpha >= beta:
            break
        
    return v


def min_value(alpha, beta, board):
    if terminal(board):
        return utility(board)

    available_actions = actions(board)
    v = math.inf

    for action in available_actions:
        v = min(v, max_value(alpha, beta, result(board, action)))
        beta = min(beta, v)

        if alpha >= beta:
            break

    return v