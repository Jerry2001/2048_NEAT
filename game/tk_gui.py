from game import utils
from game.utils import Direction
from tkinter import *

WINDOW_SIZE = 1000
BOARD_DISPLAY_SIZE = 500
GRID_PADDING = 5
EMPTY_TILE = 0
FONT = ("Helvetica", 40, "bold")


class GameGUI(Frame):
    def __init__(self, game):
        self.game = game
        self.board = game.Board()
        self.board_size = len(self.board)
        self.score = game.Score()
        self.move = game.Move()
        self.max_tile = game.Max_tile()

        Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.board_grid_cells = []
        self.score_grid_cells = []
        self.direction_grid_cells = []
        self._draw_score()
        self._draw_board()

    def reset_move_count(self):
        self.move_count = 0

    def set_game(self, game):
        self.game = game

    # Should be used when tiles changed on the board
    def repaint_board(self):
        self.board = self.game.Board()
        for i in range(self.board_size):
            for j in range(self.board_size):
                val = self.board[i][j]
                if val == EMPTY_TILE:
                    self.board_grid_cells[i][j].config(text="", bg=_get_colour(EMPTY_TILE))
                else:
                    self.board_grid_cells[i][j].config(text=str(val), bg=_get_colour(val))

        self.score = self.game.Score()
        self.move = self.game.Move()
        self.max_tile = self.game.Max_tile()

        self.score_grid_cells[0].config(text="Score: " + str(self.score))
        self.score_grid_cells[1].config(text="Max Tile: " + str(self.max_tile))
        #self.score_grid_cells[1].config(text="Moves: " + str(self.move))

        self.update_idletasks()
        self.update()

    def _draw_board(self):
        background = Frame(self, bg=_get_colour(None), width=WINDOW_SIZE, height=WINDOW_SIZE)
        background.grid()
        board_frame = Frame(background, bg=_get_colour(None), width=BOARD_DISPLAY_SIZE, height=BOARD_DISPLAY_SIZE)
        board_frame.grid()
        for i in range(self.board_size):
            grid_row = []
            for j in range(self.board_size):
                cell = Frame(board_frame, bg=_get_colour(EMPTY_TILE), width=BOARD_DISPLAY_SIZE / self.board_size,
                             height=BOARD_DISPLAY_SIZE / self.board_size)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(master=cell, text="", bg=_get_colour(EMPTY_TILE), justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.board_grid_cells.append(grid_row)
        board_frame.pack()

    def _draw_score(self):
        score_frame_size = 100
        score_frame = Frame(self, width=score_frame_size / 2, height=score_frame_size)
        score_frame.grid()
        score_text = Label(master=score_frame, text="Score: " + str(self.score), justify=CENTER,
                           font=("Helvetica", 28, "bold"))
        move_count_text = Label(master=score_frame, text="Moves: " + str(self.move), justify=CENTER,
                                font=("Helvetica", 28, "bold"))
        self.score_grid_cells.append(score_text)
        self.score_grid_cells.append(move_count_text)
        score_text.grid()
        move_count_text.grid()
        self.update()

    # Shows which direction is game has been told to try move toward
    def _draw_direction(self):
        arrow_size = 50
        direction_frame = Frame(self, bg=_get_colour(None), width=BOARD_DISPLAY_SIZE / 2, height=BOARD_DISPLAY_SIZE / 2)
        direction_frame.grid()
        directions = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
        arrows = []
        colors = ["#111111", "#222222", "#333333", "#444444"]
        i = 0
        for direction in directions:
            arrow = Frame(direction_frame, bg=_get_colour(None), width=arrow_size, height=arrow_size)
            text = Label(master=arrow, text=direction, bg=colors[i], font=("Helvetica", 10, "bold"))
            text.grid()
            arrows.append(text)
            i = i + 1
        self.update()


# Coverts (r, g, b) to hex #rrggbb
def _get_colour(num):
    return '#%02x%02x%02x' % utils.get_colour(num)
