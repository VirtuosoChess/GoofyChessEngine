import numpy as np
from board import Piece

class Evaluation:
    def __init__(self):
        self.piece_values = {
            Piece.PAWN: 100, Piece.KNIGHT: 320, Piece.BISHOP: 330,
            Piece.ROOK: 500, Piece.QUEEN: 900, Piece.KING: 20000
        }
        self.piece_square_tables = self.initialize_piece_square_tables()

    def initialize_piece_square_tables(self):

        pawn_table = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        knight_table = np.array([
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20, 0, 0, 0, 0, -20, -40],
            [-30, 0, 10, 15, 15, 10, 0, -30],
            [-30, 5, 15, 20, 20, 15, 5, -30],
            [-30, 0, 15, 20, 20, 15, 0, -30],
            [-30, 5, 10, 15, 15, 10, 5, -30],
            [-40, -20, 0, 5, 5, 0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ])
        bishop_table = np.array([
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-10, 0, 5, 10, 10, 5, 0, -10],
            [-10, 5, 5, 10, 10, 5, 5, -10],
            [-10, 0, 10, 10, 10, 10, 0, -10],
            [-10, 10, 10, 10, 10, 10, 10, -10],
            [-10, 5, 0, 0, 0, 0, 5, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ])
        rook_table = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [0, 0, 0, 5, 5, 0, 0, 0]
        ])
        queen_table = np.array([
            [-20, -10, -10, -5, -5, -10, -10, -20],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-10, 0, 5, 5, 5, 5, 0, -10],
            [-5, 0, 5, 5, 5, 5, 0, -5],
            [0, 0, 5, 5, 5, 5, 0, -5],
            [-10, 5, 5, 5, 5, 5, 0, -10],
            [-10, 0, 5, 0, 0, 0, 0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20]
        ])
        king_table = np.array([
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [20, 20, 0, 0, 0, 0, 20, 20],
            [20, 30, 10, 0, 0, 10, 30, 20]
        ])
        return {
            Piece.PAWN: pawn_table, Piece.KNIGHT: knight_table,
            Piece.BISHOP: bishop_table, Piece.ROOK: rook_table,
            Piece.QUEEN: queen_table, Piece.KING: king_table
        }

    def evaluate_board(self, board):
        material_score = 0
        positional_score = 0
        mobility_score = 0

        for row in range(8):
            for col in range(8):
                piece = board.board[row, col]
                if piece != Piece.EMPTY:
                    piece_type = piece & 0b111
                    value = self.piece_values[piece_type]
                    if piece & Piece.WHITE:
                        material_score += value
                        positional_score += self.piece_square_tables[piece_type][row, col]
                        mobility_score += self.get_mobility(board, row, col, piece)
                    else:
                        material_score -= value
                        positional_score -= self.piece_square_tables[piece_type][7 - row, col]
                        mobility_score -= self.get_mobility(board, row, col, piece)

        return material_score + positional_score + mobility_score

    def get_mobility(self, board, row, col, piece):

        piece_type = piece & 0b111
        mobility = 0
        if piece_type in (Piece.BISHOP, Piece.ROOK, Piece.QUEEN):
            directions = {
                Piece.BISHOP: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
                Piece.ROOK: [(-1, 0), (1, 0), (0, -1), (0, 1)],
                Piece.QUEEN: [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
            }[piece_type]
            for dr, dc in directions:
                for i in range(1, 8):
                    new_row, new_col = row + dr * i, col + dc * i
                    if not board.is_valid_position((new_row, new_col)):
                        break
                    target_piece = board.board[new_row, new_col]
                    if target_piece == Piece.EMPTY:
                        mobility += 1
                    elif (target_piece & Piece.WHITE) != (piece & Piece.WHITE):
                        mobility += 1
                        break
                    else:
                        break
        elif piece_type == Piece.KNIGHT:
            knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
            for dr, dc in knight_moves:
                new_row, new_col = row + dr, col + dc
                if board.is_valid_position((new_row, new_col)):
                    target_piece = board.board[new_row, new_col]
                    if target_piece == Piece.EMPTY or (target_piece & Piece.WHITE) != (piece & Piece.WHITE):
                        mobility += 1

        return mobility


