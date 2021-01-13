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
        self.winning_edge = ""
        self.board = board
        self.piece_coordinates = {"row": 0, "col": 0}
        self.wall_list = []
        self.legal_moves = {"north": True,
                            "south": True,
                            "east": True,
                            "west": True}
        self.generate_starting_and_winning_edge()
        list_of_players.append(self)

    def generate_starting_and_winning_edge(self):
        if self.starting_edge == "south":
            self.piece_coordinates["row"] = self.board.actual_rows - 2
            self.piece_coordinates["col"] = math.floor(self.board.actual_cols / 2)
            self.winning_edge = "north"
        elif self.starting_edge == "north":
            self.piece_coordinates["row"] = 1
            self.piece_coordinates["col"] = math.floor(self.board.actual_cols / 2)
            self.starting_edge = "south"
        elif self.starting_edge == "east":
            self.piece_coordinates["row"] = math.floor(self.board.actual_rows / 2)
            self.piece_coordinates["col"] = self.board.actual_cols - 2
            self.winning_edge = "west"
        elif self.starting_edge == "west":
            self.piece_coordinates["row"] = math.floor(self.board.actual_rows / 2)
            self.piece_coordinates["col"] = 1
            self.winning_edge = "east"
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


def check_for_wall_on_tile(player, board):
    tile = board.tile_matrix[player.piece_coordinates["row"]][player.piece_coordinates["col"]]
    if tile.player_on is not None:
        return True
    return False


def move_piece(player, direction, list_of_players, board):
    if direction == "n":
        player.piece_coordinates["row"] -= 1
        wall_on_tile = check_for_wall_on_tile(player, board)
        if wall_on_tile:
            player.piece_coordinates["row"] += 1
            return False
        else:
            player.piece_coordinates["row"] -= 1
    elif direction == "s" and player.legal_moves["south"] is True:
        player.piece_coordinates["row"] += 1
        wall_on_tile = check_for_wall_on_tile(player, board)
        if wall_on_tile:
            player.piece_coordinates["row"] -= 1
            return False
        else:
            player.piece_coordinates["row"] += 1
    elif direction == "e" and player.legal_moves["east"] is True:
        player.piece_coordinates["col"] += 1
        wall_on_tile = check_for_wall_on_tile(player, board)
        if wall_on_tile:
            player.piece_coordinates["col"] -= 1
            return False
        else:
            player.piece_coordinates["col"] += 1
    elif direction == "w" and player.legal_moves["west"] is True:
        player.piece_coordinates["col"] -= 1
        wall_on_tile = check_for_wall_on_tile(player, board)
        if wall_on_tile:
            player.piece_coordinates["col"] += 1
            return False
        else:
            player.piece_coordinates["col"] -= 1
    else:
        return False

    change_turn(list_of_players)

    return True


def create_wall(player, move_string, list_of_players, board):
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
    change_turn(list_of_players)

    return True


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


def change_turn(list_of_players):
    for player in list_of_players:
        if player.is_their_turn:
            player.is_their_turn = False
            player_index = list_of_players.index(player)
            if player_index != len(list_of_players) - 1:
                list_of_players[player_index + 1].is_their_turn = True
            else:
                list_of_players[0].is_their_turn = True
            return
