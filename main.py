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
        quick_start = input("Use default settings? (Y/N) > ")
        if quick_start == "Y":
            return True
        elif quick_start == "N":
            return False
        else:
            print("Invalid input, type 'Y' or 'N'")
            user_input = input("> ")
            process_user_input(user_input)
    else:
        print("Invalid input, type help to see a list of valid commands.")
        user_input = input("> ")
        process_user_input(user_input)


def get_game_settings(quick_start):
    game_settings = {"rows": 0, "cols": 0, "players": 0, "walls": 0}
    if quick_start:
        game_settings["rows"] = 9
        game_settings["cols"] = 9
        game_settings["players"] = 2
        game_settings["walls"] = 10
    else:
        game_settings["rows"] = int(input("How many rows should the board have (odd number)? > "))
        game_settings["cols"] = int(input("How many columns should the board have (odd number)? > "))
        game_settings["players"] = int(input("How many players should the game have (2 or 4)? > "))
        game_settings["walls"] = int(input("How many walls should each player have? > "))
    return game_settings


def do_move(move_string, player_list, board):
    player_to_move = None
    for player in player_list:
        if player.is_their_turn:
            player_to_move = player
    if move_string[0:2] == "m_":
        Player.move_piece(player_to_move, move_string[2:])
    elif move_string[0:2] == "w_":
        Player.place_wall(player_to_move, move_string[2:], board)
    elif move_string == "pass":
        pass
    else:
        print("Invalid move, type help to see how to input moves.")
        return False
    return True


def game_loop(player_list, board, game_settings):
    valid_move = True  # so that board prints on the first turn
    while True:
        # print/update board if last move was valid
        if valid_move:
            board = Board.Board(game_settings["rows"], game_settings["cols"])
            Player.add_players_to_board(player_list, board)
            Board.print_board(board, player_list)

        # play
        move_string = input("Type a move > ")
        if move_string == "exit":
            break
        else:
            valid_move = do_move(move_string, player_list, board)
    return


if __name__ == "__main__":

    print(Text.welcome)
    user_input = input("> ")
    quick_start = process_user_input(user_input)  # only returns if game starts
    game_settings = get_game_settings(quick_start)

    # create the board
    board = Board.Board(game_settings["rows"], game_settings["cols"])

    # create the players
    Player.create_players(game_settings["players"],
                          game_settings["walls"], board)

    # play the game
    game_loop(Player.list_of_players, board, game_settings)
    print("Thank you for playing.")
