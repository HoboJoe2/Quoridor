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
        self.move_list = []
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
        self.v_wall_is_valid = True
        self.h_wall_is_valid = True
        self.player_on = None
        self.char = ""
        self.color = f"{Fore.MAGENTA}"
        self.set_initial_attributes()

    def __repr__(self):
        return f"""Tile({self.row}, {self.col},
        {self.color}{self.char} {self.board})"""

    def set_initial_attributes(self):

        # idk why -2 not -1, maybe something to do with list index
        if self.row == self.board.actual_rows - 2:
            self.v_wall_is_valid = False

        if self.col == self.board.actual_cols - 2:
            self.h_wall_is_valid = False

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
    print()

    row_indicator_length = 0
    for row in board.tile_matrix:
        row_indicator_length = len(str(board.tile_matrix.index(row)))

    col_indicators = []
    for empty_col in range(row_indicator_length + 1):
        col_indicators.append(" ")

    col_number = 0
    for col in range(len(board.tile_matrix[0])):
        if col % 2 != 0:
            col_number += 1
            col_indicators.append(col_number)
        else:
            col_indicators.append(" ")

    for char in col_indicators:
        print(f"{Fore.LIGHTBLACK_EX}{char}", end="")

    print()

    row_indicator_number = 0
    for row in board.tile_matrix:
        if board.tile_matrix.index(row) % 2 != 0:
            row_indicator_number += 1
            row_indicator = str(row_indicator_number) + (" " * (row_indicator_length - len(str(row_indicator_number))))
        else:
            row_indicator = " " * row_indicator_length
        print(f"{Fore.LIGHTBLACK_EX}{row_indicator} ", end="")
        for tile in row:
            print(tile.color + tile.char, end="")
        print()

    print()

    for player in list_of_players:
        print(f"{player.color}Walls left: {player.walls_left}")

    print()
    for player in list_of_players:
        if player.is_their_turn:
            print(f"{player.color}{player.name} to move...")
    print()

    return
