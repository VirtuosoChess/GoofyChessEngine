from board import Board, Piece
from move_generation import MoveGenerator
from evaluation import Evaluation
from search import Search

class ChessEngine:
    def __init__(self):
        self.board = Board()
        self.move_generator = MoveGenerator(self.board)
        self.evaluation = Evaluation()
        self.search = Search(self.move_generator, self.evaluation)

    def get_best_move(self, depth):
        return self.search.search(self.board, depth)

    def play(self):
        while True:
            self.board.print_board()
            if self.board.turn == Piece.WHITE:
                move = self.get_best_move(4)
            else:
                move = self.get_best_move(4)
            if move:
                from_pos, to_pos = move
                captured_piece = self.board.get_piece(to_pos)
                self.board.make_move(from_pos, to_pos)
                self.board.turn = Piece.WHITE if self.board.turn == Piece.BLACK else Piece.BLACK
            else:
                print("No legal moves available.")
                break

if __name__ == "__main__":
    engine = ChessEngine()
    engine.play()


