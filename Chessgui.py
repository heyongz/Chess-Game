import tkinter as tk
from tkinter.messagebox import askokcancel
from Chessboard import Chessboard
from Chesspiece import WHITE, BLACK


"""

   Y\X  0       1       2       3       4       5       6       7
    0   Rook	Knight	Bishop	Queen	King	Bishop	Knight	Rook
    1   Pawn	Pawn	Pawn	Pawn	Pawn	Pawn	Pawn	Pawn
    2   ____	____	____	____	____	____	____	____
    3   ____	____	____	____	____	____	____	____
    4   ____	____	____	____	____	____	____	____
    5   ____	____	____	____	____	____	____	____
    6   Pawn	Pawn	Pawn	Pawn	Pawn	Pawn	Pawn	Pawn
    7   Rook	Knight	Bishop	Queen	King	Bishop	Knight	Rook

"""


class Chessgui:
    logic = None
    window = None
    canvas = None
    src_pos = None
    dest_pos = None
    img_holder = []

    def __init__(self, logic):
        self.logic = logic
        self.init_window("800x800")
        self.init_canvas()

    def init_window(self, geometry: str):
        self.window = tk.Tk()
        self.set_title()
        self.window.geometry(geometry)
        self.window.resizable(width=False, height=False)

    def init_canvas(self):
        self.canvas = tk.Canvas(self.window, height=800, width=800)
        self.canvas.bind("<Button-1>", self.click_event)
        self.draw_canvas()
        self.canvas.pack()

    def reset_game(self):
        self.logic.reset_game()
        self.draw_canvas()
        self.set_title()

    def set_title(self):
        title = "WHITE TURN" if self.logic.turn != BLACK else "BLACK TURN"
        self.window.title(title)

    def popup_box(self):
        if not self.logic.gameover:
            return

        winner = "white" if self.logic.get_winner() == WHITE else "black"
        msg = "Winner is %s !\nStart a new game?" % winner

        if askokcancel("Game Over", msg, parent=self.window):
            self.reset_game()
        else:
            self.window.destroy()

    """ ------------------------ Click Event ------------------------ """

    def click_event(self, event):
        x, y = int(event.x / 100), int(event.y / 100)
        self.src_pos, self.dest_pos = self.dest_pos, [x, y]
        self.draw_available_moves(self.dest_pos)

        # Click only once, return and waiting for next click
        if self.src_pos is None:
            return

        if self.logic.process(self.src_pos, self.dest_pos):
            # Successfully make a movement, clear clicks
            self.src_pos = None
            self.dest_pos = None
        else:
            src = self.logic.get_piece(self.src_pos)
            dest = self.logic.get_piece(self.dest_pos)

            if src is None:
                return
            if src.color == self.logic.turn:
                if dest is None or dest.color != self.logic.turn:
                    self.dest_pos = self.src_pos
            else:
                if dest is None or dest.color != self.logic.turn:
                    self.src_pos = None
                    self.dest_pos = None
                else:
                    self.dest_pos = self.src_pos
            return

        self.draw_canvas()
        self.set_title()
        self.popup_box()

    """ ------------------------ GUI Drawing ------------------------ """

    def draw_canvas(self):
        self.img_holder = []
        board = self.logic.chessboard.board
        flag = True
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                lx, ly = i * 100, j * 100
                if flag:
                    self.canvas.create_rectangle(
                        lx, ly, lx + 100, ly + 100, fill="PeachPuff"
                    )
                else:
                    self.canvas.create_rectangle(
                        lx, ly, lx + 100, ly + 100, fill="Peru"
                    )
                if j != 7:
                    flag = not flag

                if piece is None:
                    continue
                img_path = (
                    "Resources/"
                    + ("B_" if piece.color == BLACK else "W_")
                    + piece.type
                    + ".gif"
                )
                img = tk.PhotoImage(file=img_path)
                self.canvas.create_image(lx, ly, image=img, anchor=tk.NW)
                self.img_holder.append(img)  # Avoid img being released

    def draw_moves(self, moves):
        for [x, y] in moves:
            lx, ly = x * 100, y * 100
            self.canvas.create_rectangle(
                lx, ly, lx + 100, ly + 100, outline="brown", width=4
            )

    def draw_available_moves(self, pos):
        piece = self.logic.get_piece(pos)
        if piece is None or piece.color != self.logic.turn:
            return
        self.draw_canvas()
        self.draw_moves(self.logic.available_move(pos))
