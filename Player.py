list_of_players = []


class Player:

    def __init__(self, color, goes_first, x, y):
        self.color = color
        self.walls_left = 10
        self.is_their_turn = goes_first
        self.piece_xy = {"x": x, "y": y}
        self.legal_moves = {"north": True,
                            "south": True, "east": True, "west": True}

        list_of_players.append(self)

    def __repr__(self):
        return f"Player({self.color}, {self.is_their_turn}, {self.piece_xy})"


RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)


def create_players(number_of_players):
    list_of_players = []
    if number_of_players == 2:
        blue_player = Player(BLUE, True, 8, 16)
        list_of_players.append(blue_player)

        red_player = Player(RED, False, 8, 0)
        list_of_players.append(red_player)

    elif number_of_players == 4:
        blue_player = Player(BLUE, True, 8, 16)
        list_of_players.append(blue_player)

        red_player = Player(RED, False, 8, 0)
        list_of_players.append(red_player)

        green_player = Player(GREEN, False, 0, 8)
        list_of_players.append(green_player)

        yellow_player = Player(YELLOW, False, 16, 0)
        list_of_players.append(yellow_player)
    return list_of_players


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
