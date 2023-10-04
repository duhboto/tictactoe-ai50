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


def get_next_player(board):
    """
    Returns player who has the next turn on a board.
    """
    move_count = sum(cell == 'X' or cell == 'O' for row in board for cell in row)
  
    #(Assuming X always goes first). If move count is even, it is X's turn. If odd, it's O's turn.
    return 'X' if move_count % 2 == 0 else 'O'
 
 


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making a move, action, on the board.
    """
    i, j = action
    player = get_next_player(board)
    if board[i][j] == EMPTY:
        new_board = create_new_board(board)
        new_board[i][j] = player
        return new_board
    else:
        raise Exception("Invalid action.")



def winner(board):
    lines = [
        [board[i][0] for i in range(3)],  # cols
        [board[i][1] for i in range(3)],  # cols
        [board[i][2] for i in range(3)],  # cols
        board[0],  # rows
        board[1],  # rows
        board[2],  # rows
        [board[i][i] for i in range(3)],  # main diagonal
        [board[i][2 - i] for i in range(3)]  # antisec diagonal
    ]
    if [X, X, X] in lines:
        return X
    elif [O, O, O] in lines:
        return O
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or not any(EMPTY in row for row in board)



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
        _, move = max_value(board)
        return move
    else:
        _, move = min_value(board)
        return move
    
def max_value(board):
    if terminal(board):
        return utility(board), None
    v = -math.inf
    move = None
    for action in actions(board):
        min_v, _ = min_value(result(board, action))
        if min_v > v:
            v = min_v
            move = action
            if v == 1:
                return v, move
    return v, move

def min_value(board):
    if terminal(board):
        return utility(board), None
    v = math.inf
    move = None
    for action in actions(board):
        max_v, _ = max_value(result(board, action))
        if max_v < v:
            v = max_v
            move = action
            if v == -1:
                return v, move
    return v, move


