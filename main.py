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


# draw the board and get the dimensions
# (in order to draw the pieces and walls)
cur_board = Board.create_board(9, 9)

if __name__ == "__main__":

    # create the players
    number_of_players = 2  # TODO give player choice
    players_list = Player.create_players(number_of_players)

    # draw the board
    Board.draw_board(cur_board)

    # draw the pieces
    Player.draw_pieces(cur_board)

    player_to_move = Player.get_current_player(players_list)
