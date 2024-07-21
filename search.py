class Search:
    def __init__(self, move_generator, evaluation):
        self.move_generator = move_generator
        self.evaluation = evaluation
        self.transposition_table = {}

    def search(self, board, depth):
        best_move = None
        best_value = -float('inf')
        moves = self.move_generator.generate_legal_moves()
        
        for move in moves:
            from_pos, to_pos = move
            captured_piece = board.make_move(from_pos, to_pos)
            board_value = self.minimax(board, depth - 1, -float('inf'), float('inf'), False)
            board.undo_move(from_pos, to_pos, captured_piece)
            if board_value > best_value:
                best_value = board_value
                best_move = move
                
        return best_move

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0:
            return self.evaluation.evaluate_board(board)

        board_key = tuple(map(tuple, board.board))
        if board_key in self.transposition_table:
            return self.transposition_table[board_key]

        moves = self.move_generator.generate_legal_moves()
        if is_maximizing:
            max_eval = -float('inf')
            for move in moves:
                from_pos, to_pos = move
                captured_piece = board.make_move(from_pos, to_pos)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.undo_move(from_pos, to_pos, captured_piece)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                from_pos, to_pos = move
                captured_piece = board.make_move(from_pos, to_pos)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.undo_move(from_pos, to_pos, captured_piece)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = min_eval
            return min_eval
