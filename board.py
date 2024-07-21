import numpy as np

class Piece:
    EMPTY = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

    WHITE = 8
    BLACK = 16

class Board:
    def __init__(self):
        self.board = np.array([
            [Piece.ROOK | Piece.BLACK, Piece.KNIGHT | Piece.BLACK, Piece.BISHOP | Piece.BLACK, Piece.QUEEN | Piece.BLACK, Piece.KING | Piece.BLACK, Piece.BISHOP | Piece.BLACK, Piece.KNIGHT | Piece.BLACK, Piece.ROOK | Piece.BLACK],
            [Piece.PAWN | Piece.BLACK] * 8,
            [Piece.EMPTY] * 8,
            [Piece.EMPTY] * 8,
            [Piece.EMPTY] * 8,
            [Piece.EMPTY] * 8,
            [Piece.PAWN | Piece.WHITE] * 8,
            [Piece.ROOK | Piece.WHITE, Piece.KNIGHT | Piece.WHITE, Piece.BISHOP | Piece.WHITE, Piece.QUEEN | Piece.WHITE, Piece.KING | Piece.WHITE, Piece.BISHOP | Piece.WHITE, Piece.KNIGHT | Piece.WHITE, Piece.ROOK | Piece.WHITE]
        ])
        self.turn = Piece.WHITE

    def get_piece(self, pos):
        row, col = pos
        return self.board[row, col]

    def set_piece(self, pos, piece):
        row, col = pos
        self.board[row, col] = piece

    def make_move(self, from_pos, to_pos):
        piece = self.get_piece(from_pos)
        captured_piece = self.get_piece(to_pos)
        self.set_piece(to_pos, piece)
        self.set_piece(from_pos, Piece.EMPTY)
        return captured_piece

    def undo_move(self, from_pos, to_pos, captured_piece):
        piece = self.get_piece(to_pos)
        self.set_piece(from_pos, piece)
        self.set_piece(to_pos, captured_piece)

    def is_valid_position(self, pos):
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8

    def print_board(self):
        piece_symbols = {
            Piece.PAWN | Piece.WHITE: 'P', Piece.PAWN | Piece.BLACK: 'p',
            Piece.KNIGHT | Piece.WHITE: 'N', Piece.KNIGHT | Piece.BLACK: 'n',
            Piece.BISHOP | Piece.WHITE: 'B', Piece.BISHOP | Piece.BLACK: 'b',
            Piece.ROOK | Piece.WHITE: 'R', Piece.ROOK | Piece.BLACK: 'r',
            Piece.QUEEN | Piece.WHITE: 'Q', Piece.QUEEN | Piece.BLACK: 'q',
            Piece.KING | Piece.WHITE: 'K', Piece.KING | Piece.BLACK: 'k'
        }
        for row in self.board:
            print(" ".join(piece_symbols.get(piece, '.') for piece in row))
