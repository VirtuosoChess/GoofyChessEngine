import numpy as np
from board import Board, Piece

class MoveGenerator:
    def __init__(self, board):
        self.board = board

    def generate_legal_moves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row, col]
                if piece and (piece & Piece.WHITE) == self.board.turn:
                    moves.extend(self.generate_piece_moves((row, col), piece))
        return moves

    def generate_piece_moves(self, pos, piece):
        piece_type = piece & 0b111
        if piece_type == Piece.PAWN:
            return self.generate_pawn_moves(pos, piece)
        elif piece_type == Piece.KNIGHT:
            return self.generate_knight_moves(pos, piece)
        elif piece_type == Piece.BISHOP:
            return self.generate_bishop_moves(pos, piece)
        elif piece_type == Piece.ROOK:
            return self.generate_rook_moves(pos, piece)
        elif piece_type == Piece.QUEEN:
            return self.generate_queen_moves(pos, piece)
        elif piece_type == Piece.KING:
            return self.generate_king_moves(pos, piece)
        return []

    def generate_pawn_moves(self, pos, piece):
        moves = []
        row, col = pos
        direction = -1 if piece & Piece.WHITE else 1
        start_row = 6 if piece & Piece.WHITE else 1

        new_row = row + direction
        if self.board.is_valid_position((new_row, col)) and self.board.board[new_row, col] == Piece.EMPTY:
            moves.append(((row, col), (new_row, col)))

            if row == start_row:
                new_row += direction
                if self.board.is_valid_position((new_row, col)) and self.board.board[new_row, col] == Piece.EMPTY:
                    moves.append(((row, col), (new_row, col)))

        for dc in [-1, 1]:
            new_col = col + dc
            if self.board.is_valid_position((new_row, new_col)):
                target_piece = self.board.board[new_row, new_col]
                if target_piece != Piece.EMPTY and (target_piece & Piece.WHITE) != (piece & Piece.WHITE):
                    moves.append(((row, col), (new_row, new_col)))

        return moves

    def generate_knight_moves(self, pos, piece):
        moves = []
        row, col = pos
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            new_pos = (row + dr, col + dc)
            if self.board.is_valid_position(new_pos):
                target_piece = self.board.board[new_pos]
                if target_piece == Piece.EMPTY or (target_piece & Piece.WHITE) != (piece & Piece.WHITE):
                    moves.append(((row, col), new_pos))
        return moves

    def generate_bishop_moves(self, pos, piece):
        return self.generate_sliding_moves(pos, piece, [(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def generate_rook_moves(self, pos, piece):
        return self.generate_sliding_moves(pos, piece, [(-1, 0), (1, 0), (0, -1), (0, 1)])

    def generate_queen_moves(self, pos, piece):
        return self.generate_sliding_moves(pos, piece, [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)])

    def generate_king_moves(self, pos, piece):
        moves = []
        row, col = pos
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in king_moves:
            new_pos = (row + dr, col + dc)
            if self.board.is_valid_position(new_pos):
                target_piece = self.board.board[new_pos]
                if target_piece == Piece.EMPTY or (target_piece & Piece.WHITE) != (piece & Piece.WHITE):
                    moves.append(((row, col), new_pos))

        
        if self.can_castle_kingside(piece):
            moves.append(((row, col), (row, col + 2)))
        if self.can_castle_queenside(piece):
            moves.append(((row, col), (row, col - 2)))

        return moves

    def generate_sliding_moves(self, pos, piece, directions):
        moves = []
        row, col = pos
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not self.board.is_valid_position((new_row, new_col)):
                    break
                target_piece = self.board.board[new_row, new_col]
                if target_piece == Piece.EMPTY:
                    moves.append(((row, col), (new_row, new_col)))
                elif (target_piece & Piece.WHITE) != (piece & Piece.WHITE):
                    moves.append(((row, col), (new_row, new_col)))
                    break
                else:
                    break
        return moves

    def can_castle_kingside(self, piece):
        row = 0 if piece & Piece.WHITE else 7
        return (self.board.board[row, 4] & self.board.board[row, 7]) == (Piece.KING | Piece.ROOK | piece & Piece.WHITE)

    def can_castle_queenside(self, piece):
        row = 0 if piece & Piece.WHITE else 7
        return (self.board.board[row, 4] & self.board.board[row, 0]) == (Piece.KING | Piece.ROOK | piece & Piece.WHITE)


