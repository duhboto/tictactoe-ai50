import math
from copy import deepcopy

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
    x_turns = sum([row.count(X) for row in board])
    o_turns = sum([row.count(O) for row in board])

    return X if x_turns <= o_turns else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Prioritize center, then corners, then edges.
    """
    # Center
    if board[1][1] == EMPTY:
        yield (1, 1)

    # Corners
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for corner in corners:
        if board[corner[0]][corner[1]] == EMPTY:
            yield corner

    # Edges
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    for edge in edges:
        if board[edge[0]][edge[1]] == EMPTY:
            yield edge

def result(board, action):
    """
    Returns the board that results from making a move, action, on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid action.")

    new_board = deepcopy(board)
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    lines = [
        [board[i][0] for i in range(3)],  # columns
        [board[i][1] for i in range(3)],  # columns
        [board[i][2] for i in range(3)],  # columns
        board[0],  # rows
        board[1],  # rows
        board[2],  # rows
        [board[i][i] for i in range(3)],  # main diagonal
        [board[i][2 - i] for i in range(3)]  # anti-diagonal
    ]

    if [X, X, X] in lines:
        return X
    elif [O, O, O] in lines:
        return O
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or not any(cell == EMPTY for row in board for cell in row)



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        _, move = max_value(board, -math.inf, math.inf)
        return move
    else:
        _, move = min_value(board, -math.inf, math.inf)
        return move
    
def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    v = -math.inf
    move = None
    for action in actions(board):
        min_v, _ = min_value(result(board, action), alpha, beta)
        if min_v > v:
            v = min_v
            move = action
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v, move

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    v = math.inf
    move = None
    for action in actions(board):
        max_v, _ = max_value(result(board, action), alpha, beta)
        if max_v < v:
            v = max_v
            move = action
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v, move


