import Player
import Board
import Colors


def place_wall(player, board):

    Player.change_turn()
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
    number_of_players = 2  # TODO give player choice
    Player.create_players(number_of_players, board)
    Player.add_pieces_to_board_matrix(Player.list_of_players)
    board.print_board()

    player_to_move = Player.get_current_player(Player.list_of_players)
