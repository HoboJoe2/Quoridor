from Board import Board
import Text
import os
import time


class GameError(Exception):
    def __init__(self):
        print("Incorrect or illegal move, type help to see how to input moves")


def screen_clear():
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows
        _ = os.system('cls')


def load_game(game_settings, move_list):
    # create the board
    board = Board(*[v for k, v in game_settings.items()], game_settings)
    for move in move_list:
        do_move(True, move, board)

    # play the game
    game_loop(board)
    print("Thank you for playing!")
    time.sleep(1)


def get_pregame_input():
    user_input = input("> ")
    if user_input == "rules":
        print(Text.rules)
        get_pregame_input()
    elif user_input == "help":
        print(Text.help)
        get_pregame_input()
    elif user_input == "start":
        game_settings = {"rows": 9, "cols": 9, "players": 2, "walls": 10}
        user_input = input("Type 'Y' to use custom game settings, press enter to use default settings > ")
        if user_input == "Y":
            game_settings["rows"] = int(
                input("How many rows should the board have (odd number)? > "))
            game_settings["cols"] = int(
                input("How many columns should the board have (odd number)? > "))
            game_settings["players"] = int(
                input("How many players should the game have (2 or 4)? > "))
            game_settings["walls"] = int(
                input("How many walls should each player have? > "))
        return game_settings
    else:
        print("Invalid input, type help to see a list of valid commands.")
        get_pregame_input()


def do_move(replay, move, board):
    if replay:
        player_to_move = move[0]
        move = move[1]
    else:
        player_to_move = Board.get_current_player(board)
    board.move_list.append(
        (player_to_move, move))

    if move[0:2] == "m_":
        try:
            Board.move_piece(board, move[2:], player_to_move)
        except GameError:
            pass
    elif move[0:4] == "w_v_" or move[0:4] == "w_h_":
        try:
            Board.create_wall(board, move[2:], player_to_move)
        except GameError:
            pass
    elif move == "pass":
        pass
    elif move == "help":
        print(Text.move_help)
    elif move == "undo":
        load_game(board.game_settings, board.move_list[:-1])
    return


def game_loop(board):
    while True:
        # print/update board if last move was valid
        Board.refresh_board(board)
        Board.print_board(board)

        # play
        move_string = input("Type a move > ")
        if move_string == "exit":
            break
        else:
            do_move(False, move_string, board)
            screen_clear()
        Board.change_turn(board)
    return


def main():
    print(Text.welcome)
    settings = get_pregame_input()
    load_game(settings, [])


if __name__ == "__main__":
    main()
