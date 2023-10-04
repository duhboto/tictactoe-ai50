import math
from copy import deepcopy

X = "X"   # This line of code initializes a variable named 'X' and assigns it the string value "X".
O = "O"   # This line of code initializes a variable named 'O' and assigns it the string value "O".

EMPTY = None  # This line of code initializes a variable named 'EMPTY' and assigns it the value 'None'.

CENTER = (1, 1)# Define a constant for the center position

def initial_state():
    """
    Returns starting state of the board.

    This function creates and returns a 3x3 grid (list of lists) representing
    the initial state of a game board. Each cell in the grid is initialized
    with the value EMPTY, indicating that it is unoccupied.

    Returns:
        list of lists: A 3x3 grid with all cells initialized to EMPTY.
    """
    return [[EMPTY, EMPTY, EMPTY],  # Initialize the first row with EMPTY values
            [EMPTY, EMPTY, EMPTY],  # Initialize the second row with EMPTY values
            [EMPTY, EMPTY, EMPTY]]  # Initialize the third row with EMPTY values


def player(board):
    """
    Returns player who has the next turn on a board.

    This function determines the player who has the next turn based on the
    current state of the board. It counts the number of 'X' and 'O' symbols
    on the board to determine whose turn it is. The player with fewer turns
    (X or O) is the one who has the next turn.

    Args:
        board (list of lists): The current state of the game board.

    Returns:
        str: The player ('X' or 'O') who has the next turn.
    """
    # Count the number of 'X' and 'O' symbols on the board
    x_turns = sum([row.count(X) for row in board])  # Count 'X' symbols
    o_turns = sum([row.count(O) for row in board])  # Count 'O' symbols

    # Determine the player with the next turn based on the counts
    return X if x_turns <= o_turns else O  # Return 'X' if X's turns <= O's turns, otherwise return 'O'


def actions(board):
    """
    Returns a set of all possible actions (i, j) available on the board.
    Prioritizes center, then corners, then edges.

    This function generates a set of all possible actions that a player can
    take on the board. It prioritizes actions in the following order:
    1. Center: If the center square is empty, it is the first priority.
    2. Corners: If any corner square is empty, they are the second priority.
    3. Edges: If no center or corner squares are available, edges are the
       last priority.

    Args:
        board (list of lists): The current state of the game board.

    Yields:
        tuple: A tuple (i, j) representing a possible action where 'i' is the
               row index and 'j' is the column index of the empty square.
    """
    # Center: Check if the center square is empty and yield it if it is
    if board[CENTER[0]][CENTER[1]] == EMPTY:
        yield CENTER

    # Corners: Check each corner square and yield it if it is empty
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for corner in corners:
        if board[corner[0]][corner[1]] == EMPTY:
            yield corner

    # Edges: Check each edge square and yield it if it is empty
    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    for edge in edges:
        if board[edge[0]][edge[1]] == EMPTY:
            yield edge

def result(board, action):
    """
    Returns the board that results from making a move, action, on the board.

    This function takes the current state of the board and an action (i, j)
    representing a move to be made. It checks if the action is valid (the
    square is empty), creates a new board with the move applied, and returns
    the new board.

    Args:
        board (list of lists): The current state of the game board.
        action (tuple): A tuple (i, j) representing the desired move.

    Returns:
        list of lists: The new board after applying the move.
    
    Raises:
        Exception: If the action is invalid (square is not empty).
    """
    i, j = action  # Extract row and column indices from the action

    # Check if the square at (i, j) is empty; otherwise, it's an invalid action
    if board[i][j] != EMPTY:
        raise Exception("Invalid action.")

    # Create a deep copy of the board to avoid modifying the original board
    new_board = deepcopy(board)

    # Place the current player's symbol (X or O) in the specified square
    new_board[i][j] = player(board)

    return new_board  # Return the new board with the move applied


def winner(board):
    """
    Determines the winner of the game, if any.

    This function checks the current state of the game board to determine if
    there is a winner. It examines all possible winning combinations, including
    rows, columns, and diagonals, and returns 'X' if 'X' has won, 'O' if 'O'
    has won, or None if there is no winner yet.

    Args:
        board (list of lists): The current state of the game board.

    Returns:
        str or None: The winner ('X' or 'O') or None if there is no winner.
    """
    # Define the winning combinations (lines) on the board
    lines = [
        [board[i][0] for i in range(3)],     # columns
        [board[i][1] for i in range(3)],     # columns
        [board[i][2] for i in range(3)],     # columns
        board[0],                            # rows
        board[1],                            # rows
        board[2],                            # rows
        [board[i][i] for i in range(3)],     # main diagonal
        [board[i][2 - i] for i in range(3)]  # anti-diagonal
    ]

    # Check if 'X' has won
    if [X, X, X] in lines:
        return X
    # Check if 'O' has won
    elif [O, O, O] in lines:
        return O
    # If no winner is found, return None
    else:
        return None

def terminal(board):
    """
    Determines if the game is over or not.

    This function checks whether the game is over or not based on the current
    state of the game board. The game is considered over if there is a winner
    or if there are no empty cells left on the board.

    Args:
        board (list of lists): The current state of the game board.

    Returns:
        bool: True if the game is over, False otherwise.
    """
    # Check if there is a winner using the winner() function
    if winner(board) is not None:
        return True

    # Check if there are no empty cells left on the board
    # This is done by checking if any cell in the board is still EMPTY
    if not any(cell == EMPTY for row in board for cell in row):
        return True

    # If neither condition is met, the game is not over
    return False

def utility(board):
    """
    Returns the utility value of the current game state.

    This function determines the utility value of the current game state, which
    represents the outcome of the game. It returns 1 if 'X' has won the game,
    -1 if 'O' has won, and 0 if the game is a draw or still ongoing.

    Args:
        board (list of lists): The current state of the game board.

    Returns:
        int: The utility value, where 1 indicates 'X' win, -1 indicates 'O' win,
             and 0 indicates a draw or an ongoing game.
    """
    win = winner(board)  # Check if there is a winner using the winner() function

    # Return 1 if 'X' has won, -1 if 'O' has won, and 0 if it's a draw or ongoing
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    This function implements the minimax algorithm to determine the optimal
    action for the current player on the given board. It considers both the
    maximizing player (X) and the minimizing player (O) and recursively
    evaluates the possible game outcomes to find the best move.

    Args:
        board (list of lists): The current state of the game board.

    Returns:
        tuple: A tuple (i, j) representing the optimal action where 'i' is the
               row index and 'j' is the column index.
    """
    if terminal(board):
        return None  # If the game is over, return None as there are no moves to make

    if player(board) == X:
        # If it's the turn of 'X' (maximizing player), call max_value to find the optimal move
        _, move = max_value(board, -math.inf, math.inf)
        return move
    else:
        # If it's the turn of 'O' (minimizing player), call min_value to find the optimal move
        _, move = min_value(board, -math.inf, math.inf)
        return move
 
def max_value(board, alpha, beta):
    """
    Returns the maximum utility value and the corresponding action for 'X'.

    This function represents the maximizing player's (X's) perspective in the
    minimax algorithm. It recursively explores possible game states to find
    the maximum utility value and the corresponding action for 'X'.

    Args:
        board (list of lists): The current state of the game board.
        alpha (float): The current best value for the maximizing player.
        beta (float): The current best value for the minimizing player.

    Returns:
        tuple: A tuple (v, move) representing the maximum utility value (v) and
               the corresponding action (move).
    """
    if terminal(board):
        return utility(board), None  # If the game is over, return the utility value and no move

    v = -math.inf  # Initialize v to negative infinity
    move = None   # Initialize the best move to None

    # Iterate through all possible actions
    for action in actions(board):
        min_v, _ = min_value(result(board, action), alpha, beta)  # Find the minimum value from the opponent's perspective

        # Update v and move if a better move is found
        if min_v > v:
            v = min_v
            move = action

        alpha = max(alpha, v)  # Update alpha with the maximum value found

        # Prune the search if beta is less than or equal to alpha
        if beta <= alpha:
            break

    return v, move  # Return the maximum value and the corresponding move

def min_value(board, alpha, beta):
    """
    Returns the minimum utility value and the corresponding action for 'O'.

    This function represents the minimizing player's (O's) perspective in the
    minimax algorithm. It recursively explores possible game states to find
    the minimum utility value and the corresponding action for 'O'.

    Args:
        board (list of lists): The current state of the game board.
        alpha (float): The current best value for the maximizing player.
        beta (float): The current best value for the minimizing player.

    Returns:
        tuple: A tuple (v, move) representing the minimum utility value (v) and
               the corresponding action (move).
    """
    if terminal(board):
        return utility(board), None  # If the game is over, return the utility value and no move

    v = math.inf  # Initialize v to positive infinity
    move = None   # Initialize the best move to None

    # Iterate through all possible actions
    for action in actions(board):
        max_v, _ = max_value(result(board, action), alpha, beta)  # Find the maximum value from the opponent's perspective

        # Update v and move if a better move is found
        if max_v < v:
            v = max_v
            move = action

        beta = min(beta, v)  # Update beta with the minimum value found

        # Prune the search if beta is less than or equal to alpha
        if beta <= alpha:
            break

    return v, move  # Return the minimum value and the corresponding move

