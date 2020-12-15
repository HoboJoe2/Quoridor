import Player
import Board
import Text


def process_user_input(user_input):
    if user_input == "rules":
        print(Text.rules)
        user_input = input("> ")
        process_user_input(user_input)
    elif user_input == "help":
        print(Text.help)
        user_input = input("> ")
        process_user_input(user_input)
    elif user_input == "start":
        return
    else:
        print("Invalid input, type help to see a list of valid commands.")
        user_input = input("> ")
        process_user_input(user_input)


def get_game_settings():
    game_settings = {"rows": 0, "cols": 0, "players": 0, "walls": 0}
    game_settings["rows"] = int(input("How many rows should the board have (odd number)? > "))
    game_settings["cols"] = int(input("How many columns should the board have (odd number)? > "))
    game_settings["players"] = int(input("How many players should the game have (2 or 4)? > "))
    game_settings["walls"] = int(input("How many walls should each player have? > "))
    return game_settings


def game_loop(move_sting, player_to_move, board):
    Player.add_players_to_board(Player.list_of_players, board)
    board.print_board()
    
    return


def move_piece(player, direction):
    if direction == "north" and player.legal_moves["north"] is True:
        player.y -= 2
    elif direction == "south" and player.legal_moves["south"] is True:
        player.y += 2
    elif direction == "east" and player.legal_moves["east"] is True:
        player.x += 2
    elif direction == "west" and player.legal_moves["west"] is True:
        player.x -= 2
    Player.change_turn()
    return print(player, direction)


if __name__ == "__main__":

    print(Text.welcome)
    user_input = input("> ")
    process_user_input(user_input)  # only returns if game starts
    game_settings = get_game_settings()
    
    # create the board
    board = Board.Board(game_settings["rows"], game_settings["cols"])

    # create the players
    Player.create_players(game_settings["players"],
                          game_settings["walls"], board)

    # play the game
    game_loop(Player.list_of_players, Board)
    print("Thank you for playing.")
