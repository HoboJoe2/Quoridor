import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)


class Board:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.actual_rows = ((self.num_rows * 2) + 1)
        self.actual_cols = ((self.num_cols * 2) + 1)
        self.tile_matrix = []
        self.create_starting_matrix()

    def __repr__(self):
        return f"Board({self.num_rows}, {self.num_cols})"

    def create_starting_matrix(self):
        for row in range(self.actual_rows):
            cur_row = []
            for col in range(self.actual_cols):
                cur_tile = Tile(row, col, self)
                cur_row.append(cur_tile)
            self.tile_matrix.append(cur_row)
        return


class Tile:
    def __init__(self, row, col, board):
        self.row = row
        self.col = col
        self.board = board
        self.player_on = None
        self.char = ""
        self.color = f"{Fore.MAGENTA}"
        self.get_char_and_color()

    def __repr__(self):
        return f"""Tile({self.row}, {self.col},
        {self.color}{self.char} {self.board})"""

    def get_char_and_color(self):
        if self.row % 2 != 0 and self.col % 2 != 0:  # big tile
            self.char = "O"
            self.color = f"{Fore.BLACK}"
        else:
            self.color = f"{Fore.WHITE}"
            if self.row == 0 or self.row == self.board.actual_rows - 1:
                if self.col == 0 or self.col == self.board.actual_cols - 1:
                    self.char = "+"
                else:
                    self.char = "–"
            elif self.col == 0 or self.col == self.board.actual_cols - 1:
                self.char = "|"
            elif self.row % 2 != 0:  # on a row with big tiles
                self.char = "|"
            elif self.col % 2 != 0:  # on a col with big tiles
                self.char = "–"
            elif self.row % 2 == 0 and self.col % 2 == 0:  # on an intersection
                self.char = "+"
            return


def print_board(board, list_of_players):
    for row in board.tile_matrix:
        for tile in row:
            print(tile.color + tile.char, end="")
        print()
    print()
    for player in list_of_players:
        print(f"{player.color}Walls left: {player.walls_left}")
    print()
    return
