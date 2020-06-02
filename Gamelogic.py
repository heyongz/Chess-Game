from Chessgui import *


class Gamelogic:
    def __init__(self, chessboard):
        self.turn = WHITE
        self.gameover = False
        self.chessboard = chessboard

        self.white_pos = [4, 7]
        self.black_pos = [4, 0]

    def get_piece(self, pos: list):
        [x, y] = pos
        return self.chessboard.board[x][y]

    def set_piece(self, pos, piece):
        [x, y] = pos
        if piece is not None:
            piece.pos = pos
        self.chessboard.board[x][y] = piece

    def get_winner(self):
        if self.gameover:
            if self.get_king(WHITE).checked: return BLACK
            return WHITE

    def get_king(self, color):
        pos = self.white_pos if color == WHITE else self.black_pos
        return self.get_piece(pos)

    def can_move(self, src: list, dest: list):
        src_piece = self.get_piece(src)
        dest_piece = self.get_piece(dest)

        if not src_piece.can_move(dest, self.chessboard.board): return False

        self.set_piece(src, None)
        self.set_piece(dest, src_piece)

        king_pos = dest if src_piece.type == "King" else self.get_king(src_piece.color).pos
        king = self.get_piece(king_pos)

        checked = True if king.being_checked(king.pos, self.chessboard.board) else False

        self.set_piece(src, src_piece)
        self.set_piece(dest, dest_piece)

        return False if checked else True

    def move_piece(self, src: list, dest: list):
        piece = self.get_piece(src)
        board = self.chessboard.board
        if piece.type == "King":
            if piece.color == WHITE: self.white_pos = dest
            else: self.black_pos = dest
        piece.move_piece(dest, board)

    def available_move(self, src):
        res = []
        for i in range(8):
            for j in range(8):
                dest = [i, j]
                if self.can_move(src, dest):
                    res.append(dest)
        return res

    def game_over(self):
        w_king, b_king = self.get_king(WHITE), self.get_king(BLACK)
        if not w_king.checked and not b_king.checked:
            self.gameover = False
            return self.gameover

        for i in range(8):
            for j in range(8):
                piece = self.get_piece([i, j])
                if piece is None: continue
                if piece.color != self.turn: continue
                moves = self.available_move([i, j])
                if len(moves) != 0:
                    self.gameover = False
                    return self.gameover

        self.gameover = True
        return self.gameover

    def reset_game(self):
        self.chessboard.reset_board()
        self.__init__(self.chessboard)

    def process(self, pre, cur):
        pre_piece = self.get_piece(pre)
        cur_piece = self.get_piece(cur)

        if pre_piece is None: return False
        if pre_piece.color != self.turn: return False
        if cur_piece is not None and pre_piece.color == cur_piece.color: return False

        if self.can_move(pre, cur):
            self.move_piece(pre, cur)
            # once we made a move, it means that our king is no long being checked
            self.get_king(self.get_piece(cur).color).checked = False

            king_pos = self.white_pos if self.turn == BLACK else self.black_pos
            king = self.get_piece(king_pos)

            if king.being_checked(king.pos, self.chessboard.board):
                king.checked = True
            else:
                king.checked = False

            self.turn = WHITE if self.turn == BLACK else BLACK
            return True
        return False


if __name__ == "__main__":
    gui = Chessgui(Gamelogic(Chessboard()))
    gui.window.mainloop()







