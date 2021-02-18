from board import Board
import text
import os
import colorama
from colorama import Fore, Back, Style
import time

colorama.init(autoreset=True)


def process_user_input(user_input):
    if user_input == "rules":
        print(text.rules)
        user_input = input("> ")
        process_user_input(user_input)
    elif user_input == "help":
        print(text.help)
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
        game_settings["rows"] = int(
            input("How many rows should the board have (odd number)? > "))
        game_settings["cols"] = int(
            input("How many columns should the board have (odd number)? > "))
        game_settings["players"] = int(
            input("How many players should the game have (2 or 4)? > "))
        game_settings["walls"] = int(
            input("How many walls should each player have? > "))
    return game_settings


def do_move(move_string, board):
    player_to_move = Board.get_current_player(board)

    if move_string[0:2] == "m_":
        valid_move = Board.move_piece(board, move_string[2:], player_to_move)
        if not valid_move:
            return False
    elif move_string[0:4] == "w_v_" or move_string[0:4] == "w_h_":
        valid_move = Board.create_wall(board, move_string[2:], player_to_move)
        if not valid_move:
            return False
    elif move_string == "pass":
        pass
    else:
        return False

    return True


def game_loop(board):
    valid_move = True  # so that board prints on the first turn
    while True:
        # print/update board if last move was valid
        Board.add_players_to_board(board)
        Board.print_board(board)

        # play
        move_string = input("Type a move > ")
        if move_string == "exit":
            break
        elif move_string == "help":
            # in this function so it doesnt say invalid move
            print(text.move_help)
        else:
            board.move_list.append(
                (Board.get_current_player(board), move_string))
            valid_move = do_move(move_string, board)
            os.system("cls")
            if not valid_move:
                print(f"{Fore.RED}Invalid move, type help to see how to input moves")

        Board.change_turn(board)

    return


if __name__ == "__main__":

    print(text.welcome)
    user_input = input("> ")
    quick_start = process_user_input(user_input)  # only returns if game starts
    game_settings = get_game_settings(quick_start)

    # create the board
    board = Board(game_settings["rows"], game_settings["cols"], game_settings["players"],
                  game_settings["walls"])

    # play the game
    game_loop(board)
    print("Thank you for playing!")
    time.sleep(1)
