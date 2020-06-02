from Chesspiece import *


class Chessboard:
    def __init__(self):
        bd = [[None for _ in range(8)] for _ in range(8)]

        bd[0][0] = Rook([0, 0], BLACK)
        bd[7][0] = Rook([7, 0], BLACK)
        bd[1][0] = Knight([1, 0], BLACK)
        bd[6][0] = Knight([6, 0], BLACK)
        bd[2][0] = Bishop([2, 0], BLACK)
        bd[5][0] = Bishop([5, 0], BLACK)
        bd[3][0] = Queen([3, 0], BLACK)
        bd[4][0] = King([4, 0], BLACK)

        bd[0][7] = Rook([0, 7], WHITE)
        bd[7][7] = Rook([7, 7], WHITE)
        bd[1][7] = Knight([1, 7], WHITE)
        bd[6][7] = Knight([6, 7], WHITE)
        bd[2][7] = Bishop([2, 7], WHITE)
        bd[5][7] = Bishop([5, 7], WHITE)
        bd[3][7] = Queen([3, 7], WHITE)
        bd[4][7] = King([4, 7], WHITE)

        for i in range(8):
            bd[i][1] = Pawn([i, 1], BLACK)
            bd[i][6] = Pawn([i, 6], WHITE)

        self.board = bd

    def reset_board(self):
        self.__init__()
