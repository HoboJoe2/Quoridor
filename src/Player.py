import colorama
from colorama import Fore, Back, Style
import Board
import math

colorama.init(autoreset=True)


class Player:

    def __init__(self, name, walls_left, color, goes_first, starting_edge, board):
        self.name = name
        self.walls_left = walls_left
        self.color = color
        self.is_their_turn = goes_first
        self.starting_edge = starting_edge
        self.board = board
        self.piece_coordinates = {"row": 0, "col": 0}
        self.wall_list = []
        self.generate_starting_coordinates()
        board.player_list.append(self)

    def generate_starting_coordinates(self):
        if self.starting_edge == "south":
            self.piece_coordinates["row"] = self.board.actual_rows - 2
            self.piece_coordinates["col"] = math.floor(self.board.actual_cols / 2)
        elif self.starting_edge == "north":
            self.piece_coordinates["row"] = 1
            self.piece_coordinates["col"] = math.floor(self.board.actual_cols / 2)
        elif self.starting_edge == "east":
            self.piece_coordinates["row"] = math.floor(self.board.actual_rows / 2)
            self.piece_coordinates["col"] = self.board.actual_cols - 2
        elif self.starting_edge == "west":
            self.piece_coordinates["row"] = math.floor(self.board.actual_rows / 2)
            self.piece_coordinates["col"] = 1
        return

    def __repr__(self):
        return f"Player({self.color}, {self.is_their_turn}, {self.piece_coordinates})"


def add_players_to_board(board):

    add_pieces_to_tile_matrix(board)
    add_walls_to_tile_matrix(board)
    color_board_edges(board)

    return


def add_pieces_to_tile_matrix(board):
    for player in board.player_list:
        for row in board.tile_matrix:
            if board.tile_matrix.index(row) == player.piece_coordinates["row"]:
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
