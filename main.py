import Player
import Board
import Colors


def do_turn(move_sting, player_to_move, board):
    Player.add_pieces_to_tile_matrix(Player.list_of_players, board)
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

    # create the board
    board = Board.Board(9, 9)

    # create the players
    number_of_players = 4  # TODO give player choice
    Player.create_players(number_of_players, board)

    # play the game
    do_turn(None, None, board)
