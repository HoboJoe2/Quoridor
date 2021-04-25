from Board import Board
import Text
import os
import colorama
from colorama import Fore
import time

colorama.init(autoreset=True)


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
        else:
            pass
        return game_settings
    else:
        print("Invalid input, type help to see a list of valid commands.")
        get_pregame_input()


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
        Board.refresh_board(board)
        Board.print_board(board)

        # play
        move_string = input("Type a move > ")
        if move_string == "exit":
            break
        elif move_string == "help":
            # in this function so it doesnt say invalid move
            print(Text.move_help)
        else:
            board.move_list.append(
                (Board.get_current_player(board), move_string))
            valid_move = do_move(move_string, board)
            os.system("cls")
            if not valid_move:
                print(f"{Fore.RED}Invalid move, type help to see how to input moves")

        Board.change_turn(board)

    return


def main():
    print(Text.welcome)
    game_settings = get_pregame_input()

    # create the board
    board = Board(*[v for k, v in game_settings.items()])

    # play the game
    game_loop(board)
    print("Thank you for playing!")
    time.sleep(1)


if __name__ == "__main__":
    main()
