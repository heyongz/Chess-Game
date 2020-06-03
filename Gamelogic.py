from Chessgui import Chessgui
from Chessboard import Chessboard
from Chesspiece import Chesspiece, WHITE, BLACK


class Gamelogic:
    def __init__(self, chessboard):
        self.turn = WHITE
        self.gameover = False
        self.chessboard = chessboard
        self.move_num = 0

        self.white_pos = [4, 7]
        self.black_pos = [4, 0]

    """ ------------------------ Helper Functions ------------------------ """

    def get_piece(self, pos: list):
        [x, y] = pos
        return self.chessboard.board[x][y]

    def set_piece(self, pos: list, piece: Chesspiece, move_num: int):
        [x, y] = pos
        if piece is not None:
            piece.pos = pos
            piece.move_num = move_num
        self.chessboard.board[x][y] = piece

    def get_winner(self):
        if not self.gameover:
            return None
        return BLACK if self.get_king(WHITE).checked else WHITE

    def get_king(self, color: int):
        pos = self.white_pos if color == WHITE else self.black_pos
        return self.get_piece(pos)

    def reset_game(self):
        self.chessboard.reset_board()
        self.__init__(self.chessboard)

    def move_piece(self, src: list, dest: list):
        piece = self.get_piece(src)
        board = self.chessboard.board
        if piece.type == "King":
            if piece.color == WHITE:
                self.white_pos = dest
            else:
                self.black_pos = dest
        piece.move_piece(dest, board, self.move_num)
        self.move_num += 1

    def available_move(self, pos: list):
        res = []
        for i in range(8):
            for j in range(8):
                dest = [i, j]
                if self.can_move(pos, dest):
                    res.append(dest)
        return res

    """ ------------------------ Main Logic ------------------------ """

    def process(self, src_pos, dest_pos):
        src_piece = self.get_piece(src_pos)
        dest_piece = self.get_piece(dest_pos)

        if src_piece is None or src_piece.color != self.turn:
            return False
        if dest_piece is not None and src_piece.color == dest_piece.color:
            return False

        if self.can_move(src_pos, dest_pos):
            self.move_piece(src_pos, dest_pos)
            # once we made a move, it means that our king is no long being checked
            self.get_king(self.get_piece(dest_pos).color).checked = False

            king_pos = self.white_pos if self.turn == BLACK else self.black_pos
            king = self.get_piece(king_pos)

            if king.being_checked(king.pos, self.chessboard.board, self.move_num):
                king.checked = True
            else:
                king.checked = False

            self.turn = WHITE if self.turn == BLACK else BLACK
            self.game_over()  # check if game is over
            return True
        return False

    def can_move(self, src: list, dest: list):
        src_piece = self.get_piece(src)
        dest_piece = self.get_piece(dest)

        if not src_piece.can_move(dest, self.chessboard.board, self.move_num):
            return False

        src_move_num = src_piece.move_num if src_piece is not None else None
        dest_move_num = dest_piece.move_num if dest_piece is not None else None

        self.set_piece(src, None, None)
        self.set_piece(dest, src_piece, self.move_num)

        king_pos = (
            dest if src_piece.type == "King" else self.get_king(src_piece.color).pos
        )

        king = self.get_piece(king_pos)

        checked = (
            True
            if king.being_checked(king.pos, self.chessboard.board, self.move_num+1)
            else False
        )

        self.set_piece(src, src_piece, src_move_num)
        self.set_piece(dest, dest_piece, dest_move_num)

        return False if checked else True

    def game_over(self):
        w_king, b_king = self.get_king(WHITE), self.get_king(BLACK)
        if not w_king.checked and not b_king.checked:
            return

        for i in range(8):
            for j in range(8):
                pos = [i, j]
                piece = self.get_piece(pos)
                if piece is None or piece.color != self.turn:
                    continue
                if len(self.available_move(pos)) != 0:
                    return

        self.gameover = True


if __name__ == "__main__":
    gui = Chessgui(Gamelogic(Chessboard()))
    gui.window.mainloop()
