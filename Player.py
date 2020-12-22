import colorama
from colorama import Fore, Back, Style
import Board
import math

colorama.init(autoreset=True)

list_of_players = []


class Player:

    def __init__(self, walls_left, color, goes_first, starting_edge, board):
        self.color = color
        self.walls_left = walls_left
        self.is_their_turn = goes_first
        self.starting_edge = starting_edge
        self.board = board
        self.piece_coordinates = {"row": 0, "col": 0}
        self.wall_list = []
        self.legal_moves = {"north": True,
                            "south": True,
                            "east": True,
                            "west": True}
        self.generate_starting_position()
        list_of_players.append(self)

    def generate_starting_position(self):
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


def create_players(number_of_players, walls, board):
    list_of_players = []
    if number_of_players == 2:
        blue_player = Player(walls, Fore.BLUE, True, "south", board)
        list_of_players.append(blue_player)

        red_player = Player(walls, Fore.RED, False, "north", board)
        list_of_players.append(red_player)

    elif number_of_players == 4:
        blue_player = Player(walls, Fore.BLUE, True, "south", board)
        list_of_players.append(blue_player)

        red_player = Player(walls, Fore.RED, False, "north", board)
        list_of_players.append(red_player)

        green_player = Player(walls, Fore.GREEN, False, "east", board)
        list_of_players.append(green_player)

        yellow_player = Player(walls, Fore.YELLOW, False, "west", board)
        list_of_players.append(yellow_player)
    return


def add_players_to_board(list_of_players, board):
    add_pieces_to_tile_matrix(list_of_players, board)
    add_walls_to_tile_matrix(list_of_players, board)
    color_board_edges(list_of_players, board)
    return


def add_pieces_to_tile_matrix(list_of_players, board):
    for player in list_of_players:
        for row in board.tile_matrix:
            if board.tile_matrix.index(row) == player.piece_coordinates["row"]:
                for tile in row:
                    if row.index(tile) == player.piece_coordinates["col"]:
                        tile.player_on = player
                        tile.color = player.color
    return


def add_walls_to_tile_matrix(list_of_players, board):
    for player in list_of_players:
        for wall in player.wall_list:
            for row in board.tile_matrix:
                if board.tile_matrix.index(row) == wall[0]:
                    for tile in row:
                        if row.index(tile) == wall[1]:
                            tile.player_on = player
                            tile.color = player.color
    return


def create_wall(player, coordinates):
    wall_row = int(coordinates[0]) - 1  # to match list index
    wall_col = int(coordinates[1]) - 1
    player.wall_list.append([wall_row, wall_col])
    return


def color_board_edges(list_of_players, board):
    for player in list_of_players:
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


def get_current_player(players_list):
    for player in players_list:
        if player.is_their_turn:
            return player


def change_turn():
    for player in list_of_players:
        if player.is_their_turn:
            player.is_their_turn = False
            player_index = list_of_players.index(player)
            if player_index != len(list_of_players) - 1:
                list_of_players[player_index + 1].is_their_turn = True
            else:
                list_of_players[0].is_their_turn = True
            return


def move_piece(player, direction):
    if direction == "north" and player.legal_moves["north"] is True:
        player.piece_coordinates["row"] -= 2
    elif direction == "south" and player.legal_moves["south"] is True:
        player.piece_coordinates["row"] += 2
    elif direction == "east" and player.legal_moves["east"] is True:
        player.piece_coordinates["col"] += 2
    elif direction == "west" and player.legal_moves["west"] is True:
        player.piece_coordinates["col"] -= 2

    change_turn()

    return
