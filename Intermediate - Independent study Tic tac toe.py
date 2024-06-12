import tkinter as tk
from tkinter import font, messagebox
from itertools import cycle
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)

class TicTacToeGame:
    def __init__(self, board_size=BOARD_SIZE, symbols_to_win=3, players=DEFAULT_PLAYERS):
        self.board_size = board_size
        self.symbols_to_win = symbols_to_win
        self._players = cycle(players)
        self.current_player = next(self._players)
        self.winner_combo = []
        self._has_winner = False
        self._current_moves = self._setup_board()
        self._winning_combos = self._get_winning_combos()
        self._score = {player.label: 0 for player in players}
        self._score['Ties'] = 0

    def _setup_board(self):
        return [[Move(row, col) for col in range(self.board_size)] for row in range(self.board_size)]

    def _get_winning_combos(self):
        rows = [[(move.row, move.col) for move in row] for row in self._current_moves]
        columns = [list(col) for col in zip(*rows)]
        diagonals = [[(i, i) for i in range(self.board_size)], [(i, self.board_size - 1 - i) for i in range(self.board_size)]]
        return rows + columns + diagonals

    def is_valid_move(self, move):
        return self._current_moves[move.row][move.col].label == "" and not self._has_winner

    def process_move(self, move):
        self._current_moves[move.row][move.col] = move
        for combo in self._winning_combos:
            if all(self._current_moves[row][col].label == move.label for row, col in combo):
                self._has_winner = True
                self.winner_combo = combo
                self._score[move.label] += 1
                return

    def has_winner(self):
        return self._has_winner

    def is_tied(self):
        return not self._has_winner and all(move.label != "" for row in self._current_moves for move in row)

    def toggle_player(self):
        self.current_player = next(self._players)

    def reset_game(self):
        self._current_moves = self._setup_board()
        self._has_winner = False
        self.winner_combo = []

class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._game = game
        self._cells = {}
        self._font_size = 14
        self._create_menu()
        self._create_board_display()
        self._create_board_canvas()
        self.bind("<Control-plus>", self._zoom_in)
        self.bind("<Control-minus>", self._zoom_out)
        self._draw_board()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_canvas(self):
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.board_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.board_frame, anchor="nw")
        self.board_frame.bind("<Configure>", self._on_frame_configure)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _draw_board(self):
        for row in range(self._game.board_size):
            self.board_frame.grid_rowconfigure(row, weight=1, minsize=50)
            self.board_frame.grid_columnconfigure(row, weight=1, minsize=50)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=self.board_frame,
                    text="",
                    font=font.Font(size=self._font_size, weight="bold"),
                    width=5,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                button.bind("<ButtonPress-1>", self.play)

    def play(self, event):
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

    def _zoom_in(self, event):
        self._font_size += 2
        self._redraw_board()

    def _zoom_out(self, event):
        if self._font_size > 6:
            self._font_size -= 2
            self._redraw_board()

    def _redraw_board(self):
        for button in self._cells.keys():
            button.config(font=font.Font(size=self._font_size, weight="bold"))

class StartMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe Game Setup")
        self._create_widgets()

    def _create_widgets(self):
        self.board_size_label = tk.Label(self, text="Board Size:")
        self.board_size_label.pack(pady=10)
        self.board_size_entry = tk.Entry(self)
        self.board_size_entry.pack(pady=10)

        self.symbols_to_win_label = tk.Label(self, text="Symbols to Win:")
        self.symbols_to_win_label.pack(pady=10)
        self.symbols_to_win_entry = tk.Entry(self)
        self.symbols_to_win_entry.pack(pady=10)

        start_button = tk.Button(self, text="Start Game", font=font.Font(size=14), command=self.start_game)
        start_button.pack(pady=20)

    def start_game(self):
        try:
            board_size = int(self.board_size_entry.get())
            symbols_to_win = int(self.symbols_to_win_entry.get())

            if symbols_to_win > board_size:
                messagebox.showerror(
                    "Invalid Input",
                    "Symbols to win cannot be greater than board size."
                )
                return

            self.destroy()
            game = TicTacToeGame(board_size=board_size, symbols_to_win=symbols_to_win)
            board = TicTacToeBoard(game)
            board.mainloop()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for board size and symbols to win.")

if __name__ == "__main__":
    start_menu = StartMenu()
    start_menu.mainloop()
