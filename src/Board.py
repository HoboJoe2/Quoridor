import colorama
import Player
from colorama import Fore, Back, Style

colorama.init(autoreset=True)


class Board:
    def __init__(self, num_rows, num_cols, num_players, player_wall_count):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.actual_rows = ((self.num_rows * 2) + 1)
        self.actual_cols = ((self.num_cols * 2) + 1)
        self.tile_matrix = []
        self.move_list = []
        self.player_list = []
        self.create_players(num_players, player_wall_count)
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

    def create_players(self, num_players, player_wall_count):
        if num_players == 2:
            blue_player = Player.Player("Blue", player_wall_count, Fore.BLUE, True, "south", self)
            self.player_list.append(blue_player)

            red_player = Player.Player("Red", player_wall_count, Fore.RED, False, "north", self)
            self.player_list.append(red_player)

        elif num_players == 4:
            blue_player = Player.Player("Blue", player_wall_count, Fore.BLUE, True, "south", self)
            self.player_list.append(blue_player)

            red_player = Player.Player("Blue", player_wall_count, Fore.RED, False, "north", self)
            self.player_list.append(red_player)

            green_player = Player.Player("Blue", player_wall_count, Fore.GREEN, False, "east", self)
            self.player_list.append(green_player)

            yellow_player = Player.Player("Blue", player_wall_count, Fore.YELLOW, False, "west", self)
            self.player_list.append(yellow_player)
        return

    def add_pieces_to_tile_matrix(self):
        for player in self.player_list:
            for row in self.tile_matrix:
                if self.tile_matrix.index(row) == player.piece_coordinates["row"]:
                    for tile in row:
                        if row.index(tile) == player.piece_coordinates["col"]:
                            tile.player_on = player
                            tile.color = player.color
        return


    def add_walls_to_tile_matrix(board):
        for player in board.player_list:
            for wall in player.wall_list:
                for row in board.tile_matrix:
                    if board.tile_matrix.index(row) == wall[0]:
                        for tile in row:
                            if row.index(tile) == wall[1]:
                                tile.player_on = player
                                tile.color = player.color
        return


    def add_players_to_board(board):

        add_pieces_to_tile_matrix(board)
        add_walls_to_tile_matrix(board)
        color_board_edges(board)

        return


    def check_for_wall_on_tile(player, board):
        tile = board.tile_matrix[player.piece_coordinates["row"]][player.piece_coordinates["col"]]
        if tile.player_on is not None:
            return True
        return False


    def move_piece(player, direction, board):

        current_tile = board.tile_matrix[player.piece_coordinates["row"]][player.piece_coordinates["col"]]
        current_tile.player_on = None
        current_tile.color = Fore.BLACK

        if direction == "n":
            player.piece_coordinates["row"] -= 1
            wall_on_tile = check_for_wall_on_tile(player, board)
            if wall_on_tile:
                player.piece_coordinates["row"] += 1
                return False
            else:
                player.piece_coordinates["row"] -= 1

        elif direction == "s":
            player.piece_coordinates["row"] += 1
            wall_on_tile = check_for_wall_on_tile(player, board)
            if wall_on_tile:
                player.piece_coordinates["row"] -= 1
                return False
            else:
                player.piece_coordinates["row"] += 1

        elif direction == "e":
            player.piece_coordinates["col"] += 1
            wall_on_tile = check_for_wall_on_tile(player, board)
            if wall_on_tile:
                player.piece_coordinates["col"] -= 1
                return False
            else:
                player.piece_coordinates["col"] += 1

        elif direction == "w":
            player.piece_coordinates["col"] -= 1
            wall_on_tile = check_for_wall_on_tile(player, board)
            if wall_on_tile:
                player.piece_coordinates["col"] += 1
                return False
            else:
                player.piece_coordinates["col"] -= 1

        else:
            return False

        return True


    def create_wall(player, move_string, board):
        coordinates = move_string[2:]

        if player.walls_left == 0:
            return False

        elif move_string[0:2] == "h_":

            wall_row = (int(coordinates.split("_")[0]) * 2) - 2
            wall_col = (int(coordinates.split("_")[1]) * 2) - 1

            for num in [0, 1, 2]:
                if board.tile_matrix[wall_row][wall_col + num].player_on is not None:
                    return False

            for num in [0, 1, 2]:
                player.wall_list.append([wall_row, wall_col + num])

        elif move_string[0:2] == "v_":

            wall_row = (int(coordinates.split("_")[0]) * 2) - 1
            wall_col = (int(coordinates.split("_")[1]) * 2) - 2

            for num in [0, 1, 2]:
                if board.tile_matrix[wall_row + num][wall_col].player_on is not None:
                    return False

            for num in [0, 1, 2]:
                player.wall_list.append([wall_row + num, wall_col])

        else:
            return False

        player.walls_left -= 1

        return True


    def color_board_edges(board):
        for player in board.player_list:
            if player.starting_edge == "north":
                for tile in board.tile_matrix[-1][1:-1]:  # south edge
                    tile.color = player.color
            elif player.starting_edge == "south":
                for tile in board.tile_matrix[0][1:-1]:  # north edge
                    tile.color = player.color
            elif player.starting_edge == "east":  # east edge
                for row in board.tile_matrix[1:-1]:
                    for tile in row:
                        if row.index(tile) == 0:
                            tile.color = player.color
            elif player.starting_edge == "west":   # west edge
                for row in board.tile_matrix[1:-1]:
                    for tile in row:
                        if row.index(tile) == len(row) - 1:
                            tile.color = player.color
        return


    def get_current_player(board):
        for player in board.player_list:
            if player.is_their_turn:
                return player


    def change_turn(board):
        for player in board.player_list:
            if player.is_their_turn:
                player.is_their_turn = False
                player_index = board.player_list.index(player)
                if player_index != len(board.player_list) - 1:
                    board.player_list[player_index + 1].is_their_turn = True
                else:
                    board.player_list[0].is_their_turn = True
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


def print_board(board):
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

    for player in board.player_list:
        print(f"{player.color}Walls left: {player.walls_left}")

    print()
    for player in board.player_list:
        if player.is_their_turn:
            print(f"{player.color}{player.name} to move...")
    print()

    return
