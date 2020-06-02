WHITE = 1
BLACK = 0


class Chesspiece:
    def __init__(self, pos: list, color: int):
        self.pos = pos
        self.color = color
        self.moved = False
        self.type = None

    def can_move(self, dest: list, bd: list):
        [x, y] = dest
        # Within chessboard
        if not (0 <= x <= 7 and 0 <= y <= 7): return False
        # Can't overlap chess with same color
        if bd[x][y] is not None and bd[x][y].color == self.color: return False
        return True

    def move_piece(self, dest: list, bd: list):
        [dx, dy], [cx, cy] = dest, self.pos
        self.pos = dest
        self.moved = True
        bd[cx][cy] = None
        bd[dx][dy] = self


class Rook(Chesspiece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.type = "Rook"

    def can_move(self, dest: list, bd: list):
        if not super().can_move(dest, bd): return False
        [dx, dy], [cx, cy] = dest, self.pos

        # Dest and current position must be in a line
        if dx != cx and dy != cy: return False

        # Can't leap over other pieces
        if dx == cx:
            for y in range(min(dy, cy)+1, max(dy, cy)):
                if bd[dx][y] is not None: return False
        if dy == cy:
            for x in range(min(dx, cx)+1, max(dx, cx)):
                if bd[x][dy] is not None: return False

        return True


class Bishop(Chesspiece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.type = "Bishop"

    def can_move(self, dest: list, bd: list):
        if not super().can_move(dest, bd): return False
        [dx, dy], [cx, cy] = dest, self.pos

        # Dest and current position must be in a diagonal line
        if abs(dx-cx) != abs(dy-cy): return False

        delta_x = 1 if dx > cx else -1
        delta_y = 1 if dy > cy else -1

        # Can't leap over other pieces
        while True:
            cx += delta_x
            cy += delta_y
            if [cx, cy] == [dx, dy]: break
            if bd[cx][cy] is not None: return False

        return True


class Queen(Chesspiece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.type = "Queen"

    def can_move(self, dest: list, bd: list):
        if not super().can_move(dest, bd): return False

        # Queen combines the power of a rook and bishop
        tmp_rook = Rook(self.pos, self.color)
        tmp_bishop = Bishop(self.pos, self.color)

        if tmp_rook.can_move(dest, bd) or tmp_bishop.can_move(dest, bd): return True
        return False


class Knight(Chesspiece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.type = "Knight"

    def can_move(self, dest, bd):
        if not super().can_move(dest, bd): return False
        [dx, dy], [cx, cy] = dest, self.pos

        if (abs(dx-cx) == 2 and abs(dy-cy) == 1) or (abs(dx-cx) == 1 and abs(dy-cy) == 2):
            return True
        return False


class Pawn(Chesspiece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.type = "Pawn"

    def can_move(self, dest: list, bd: list):
        if not super().can_move(dest, bd): return False
        [dx, dy], [cx, cy] = dest, self.pos

        if self.color == WHITE and dy >= cy: return False
        if self.color == BLACK and dy <= cy: return False

        # moving direction of pawn
        direction = -1 if self.color == WHITE else 1

        if cx == dx:
            if abs(cy - dy) == 1:
                if bd[cx][dy] is None: return True

            if abs(cy - dy) == 2:
                if self.moved: return False
                if bd[cx][cy+direction] is None and bd[cx][dy] is None: return True
            return False

        # cx != dx
        if abs(cx - dx) != 1: return False
        if abs(cy - dy) != 1 or bd[dx][cy + direction] is None: return False
        if bd[dx][cy + direction] == self.color: return False
        return True

    def move_piece(self, dest: list, bd: list):
        super().move_piece(dest, bd)
        [x, y] = dest

        # Promotion (for simplicity, promote to queen)
        if (self.color == WHITE and y == 0) or (self.color == BLACK and y == 7):
            bd[x][y] = Queen(dest, self.color)


class King(Chesspiece):
    def __init__(self, pos: list, color: int):
        super().__init__(pos, color)
        self.type = "King"
        self.checked = False

    def can_move(self, dest: list, bd: list):
        if not super().can_move(dest, bd): return False
        [dx, dy], [cx, cy] = dest, self.pos

        # Move no more than one square or make a special move known as castling
        if abs(dx-cx) > 1 or abs(dy-cy) > 1:
            if not self.castling(dest, bd): return False

        self.pos = dest
        backup = bd[dx][dy]
        bd[cx][cy], bd[dx][dy] = None, self

        checked = self.being_checked(dest, bd)
        self.pos = [cx, cy]
        bd[cx][cy], bd[dx][dy] = self, backup

        return False if checked else True

    def being_checked(self, pos: list, bd: list):
        king_pos = None
        for i in range(8):
            for j in range(8):
                chess = bd[i][j]
                if chess is None or chess.color == self.color: continue
                # This line is to avoid infinitely loop between can_move and being_checked
                if chess.type == "King":
                    king_pos = [i, j]
                    continue
                if chess.can_move(pos, bd): return True

        # The reason that we add this if-statement is that when we call can_move in gamelogic
        # we use the src piece to overwrite dest piece. If dest piece happens to be king pos
        # when we call being_checked, we can't find king_pos. You can treat this as this king
        # is being checked because it can overwrite by piece with different color
        if king_pos is None:
            return True
        [i, j] = king_pos
        [x, y] = self.pos
        return True if abs(x-i) <= 1 and abs(y-j) <= 1 else False

    def move_piece(self, dest: list, bd: list):
        [dx, dy], [cx, cy] = dest, self.pos
        super().move_piece(dest, bd)
        self.checked = False

        # Castling
        if abs(dx-cx) > 1:
            rook = bd[0][cy] if dx < cx else bd[7][cy]
            pos = [cx-1, cy] if dx < cx else [cx+1, cy]
            rook.move_piece(pos, bd)

    def castling(self, dest: list, bd: list):
        [dx, dy], [cx, cy] = dest, self.pos
        if dy != cy: return False
        if abs(dx-cx) != 2: return False

        rook = bd[0][cy] if dx < cx else bd[7][cy]

        # Neither the king nor the rook has previously moved
        if rook is None or rook.moved or self.moved: return False

        # There are no pieces between the king and the rook
        for x in range(min(cx, dx)+1, max(cx, dx)):
            if bd[x][cy] is not None: return False

        # The king can't be in check, nor can the king pass through
        # any square that is under attack by an enemy piece
        for x in range(min(cx, dx), max(cx, dx)+1):
            if self.being_checked([x, cy], bd): return False
        return True