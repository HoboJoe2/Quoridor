import Colors
import Board
import math

list_of_players = []


class Player:

    def __init__(self, walls, color, goes_first, starting_edge, board):
        self.color = color
        self.walls = walls
        self.is_their_turn = goes_first
        self.starting_edge = starting_edge
        self.board = board
        self.piece_coordinates = {"row": 0, "col": 0}
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
        return f"Player({self.color}, {self.is_their_turn}, {self.piece_xy})"


def create_players(number_of_players, walls, board):
    list_of_players = []
    if number_of_players == 2:
        blue_player = Player(walls, Colors.BLUE, True, "south", board)
        list_of_players.append(blue_player)

        red_player = Player(walls, Colors.RED, False, "north", board)
        list_of_players.append(red_player)

    elif number_of_players == 4:
        blue_player = Player(walls, Colors.BLUE, True, "south", board)
        list_of_players.append(blue_player)

        red_player = Player(walls, Colors.RED, False, "north", board)
        list_of_players.append(red_player)

        green_player = Player(walls, Colors.GREEN, False, "east", board)
        list_of_players.append(green_player)

        yellow_player = Player(walls, Colors.YELLOW, False, "west", board)
        list_of_players.append(yellow_player)
    return


def add_players_to_board(list_of_players, board):
    add_pieces_to_tile_matrix(list_of_players, board)
    color_board_edges(list_of_players, board)
    add_walls_to_tile_matrix(list_of_players, board)
    return


def add_pieces_to_tile_matrix(list_of_players, board):
    for player in list_of_players:
        for row in board.tile_matrix:
            if board.tile_matrix.index(row) == player.piece_coordinates["row"]:
                for tile in row:
                    if row.index(tile) == player.piece_coordinates["col"]:
                        tile.color = player.color
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


def add_walls_to_tile_matrix(list_of_players, board):
    return


def get_current_player(players_list):
    for player in players_list:
        if player.is_their_turn:
            return player


def change_turn():
    for player in list_of_players:
        if player.is_their_turn is True:
            player.is_their_turn = False
            player_index = list_of_players.index(player)
            list_of_players[player_index + 1].is_their_turn = True
            return
