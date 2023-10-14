"""
Created on Wed 16 Sep 16:31 2020
Finished on Thu 17 Sep 12:00 2020
@author: Cpt.Ender

Implementation of Minimax Algorithm
with pruning for Tic Tac Toe
                                   """


def winning(board):
    """ A function to check if somebody won, if it's a tie, or if it's still going """
    transpose_board = [[board[j][i] for j in range(3)] for i in range(3)]
    outcome = None  # If the game is still going

    for piece in ['x', 'o']:
        # Check Horizontally for a outcome
        hor = [row.count(piece) == 3 for row in board]
        # Check Horizontally for a outcome
        ver = [col.count(piece) == 3 for col in transpose_board]
        # Check Diagonally for a outcome
        diag1 = board[0][0].count(piece) + board[1][1].count(piece) + board[2][2].count(piece) == 3
        diag2 = board[0][2].count(piece) + board[1][1].count(piece) + board[2][0].count(piece) == 3

        if any(hor) or any(ver) or diag1 or diag2:
            outcome = piece.capitalize()

    # Check if it's a tie
    count = 0
    for row in board:
        count += row.count('_')
    if not outcome and count == 0:
        outcome = 'Tie'
    return outcome


def minimax(board, depth, alpha, beta, MaximizingPlayer, scores):
    result = winning(board)
    current_player = whoisplayin(board)

    if result:  # If someone won
        return scores[result]
    if MaximizingPlayer:  # Maximizing Player's turn
        bestScore = -float('inf')
        for i, row in enumerate(board):
            for j, box in enumerate(row):
                if box == '_':  # if the spot is available
                    board[i][j] = current_player
                    score = minimax(board, depth - 1, alpha, beta, False, scores)
                    board[i][j] = '_'
                    bestScore = max(score, bestScore)
                    # Pruning
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return bestScore
    else:  # Minimizing Player's turn
        bestScore = float('inf')
        for i, row in enumerate(board):
            for j, box in enumerate(row):
                if box == '_':  # if the spot is available
                    board[i][j] = current_player
                    score = minimax(board, depth - 1, alpha, beta, True, scores)
                    board[i][j] = '_'
                    bestScore = min(score, bestScore)
                    # Pruning
                    beta = min(beta, score)
                    if alpha >= beta:
                        break
        return bestScore


def whoisplayin(board):
    count_x = 0
    count_o = 0
    for row in board:
        count_x += row.count('x')
        count_o += row.count('o')

    players = ['x', 'o']
    return players[count_x - count_o]


def next_move(board):
    current_player = whoisplayin(board)
    scores = {"X": 0, "O": 0, "Tie": 0, current_player.capitalize(): +1}
    keys = list(scores.keys())
    scores[keys[keys.index(current_player.capitalize()) ^ 1]] = -1
    bestScore = -float('inf')
    for i, row in enumerate(board):
        for j, box in enumerate(row):
            if box == '_':
                board[i][j] = current_player
                score = minimax(board, 0, -float('inf'), float('inf'), False, scores)
                board[i][j] = '_'
                if score > bestScore:
                    bestScore = score
                    bestMove = [i, j]
    return bestMove

# board_ = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
# move = next_move(board_)
