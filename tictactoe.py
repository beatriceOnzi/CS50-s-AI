"""
Tic Tac Toe Player
"""

import math

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
    actions = set()

    for i in range(0, 3):
        for j in range(0,3):
            if board[i][j] == EMPTY:
                actions.add(i, j)

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #board_copy = copy.deepcopy(board, memo)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return None


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    return None
