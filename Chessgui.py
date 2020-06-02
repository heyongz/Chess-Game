import tkinter as tk
import tkinter.messagebox
from Chessboard import *


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
    pre_select = None
    cur_select = None
    img_holder = []

    def __init__(self, logic):
        self.logic = logic
        self.init_window("WHITE TURN", "800x800")
        self.init_canvas()

    def init_window(self, title: str, geometry: str):
        w = tk.Tk()
        w.title(title)
        w.geometry(geometry)
        w.resizable(width=False, height=False)
        self.window = w

    def init_canvas(self):
        self.canvas = tk.Canvas(self.window, height=800, width=800)
        self.canvas.bind("<Button-1>", self.click_event)
        self.draw_canvas()
        self.canvas.pack()

    def draw_canvas(self):
        self.img_holder = []
        board = self.logic.chessboard.board
        flag = True
        for i in range(0, 8):
            for j in range(0, 8):
                lx, ly = i * 100, j * 100
                if flag: self.canvas.create_rectangle(lx, ly, lx + 100, ly + 100, fill="PeachPuff")
                else: self.canvas.create_rectangle(lx, ly, lx + 100, ly + 100, fill="Peru")
                if j != 7: flag = not flag

        for i in range(8):
            for j in range(8):
                chess = board[i][j]
                if chess is None: continue
                img_path = "Resources/" + ("B_" if chess.color == BLACK else "W_") + chess.type + ".gif"
                img = tk.PhotoImage(file=img_path)
                self.canvas.create_image(100 * i, 100 * j, image=img, anchor=tk.NW)
                # Doing this to avoid img being released by garbage recollection
                self.img_holder.append(img)

    def draw_moves(self, moves):
        for [x, y] in moves:
            lx, ly = x * 100, y * 100
            self.canvas.create_rectangle(lx, ly, lx + 100, ly + 100, outline="brown", width=4)

    def draw_available_moves(self, pos):
        piece = self.logic.get_piece(pos)

        if piece is not None and piece.color == self.logic.turn:
            self.draw_canvas()
            moves = self.logic.available_move(pos)
            self.draw_moves(moves)

    # This part needs to interact with Gamelogic
    def click_event(self, event):
        if self.logic.gameover: return
        x, y = int(event.x / 100), int(event.y / 100)
        self.pre_select, self.cur_select = self.cur_select, [x, y]
        print(self.pre_select, self.cur_select)
        # draw available moves
        self.draw_available_moves(self.cur_select)

        if self.pre_select is None: return

        if self.logic.process(self.pre_select, self.cur_select):
            self.pre_select = self.cur_select = None
        else:
            self.pre_select = self.cur_select
            return

        self.draw_canvas()
        self.change_title()

        if self.logic.game_over():
            winner = "white" if self.logic.get_winner() == WHITE else "black"
            self.popup_msg(winner)

    def reset_game(self):
        self.logic.reset_game()
        self.draw_canvas()
        self.window.title("WHITE TURN")

    def change_title(self):
        title = "WHITE TURN" if self.logic.turn == WHITE else "BLACK TURN"
        self.window.title(title)

    def popup_msg(self, winner: str):
        msg = "Winner is %s !\nStart a new game?" % winner
        reset = tk.messagebox.askokcancel('askquestion', msg, parent=self.window)
        if reset:
            self.reset_game()
        else: self.window.destroy()



if __name__ == "__main__":
    from Gamelogic import Gamelogic

    gui = Chessgui(Gamelogic(Chessboard()))
    gui.window.mainloop()

