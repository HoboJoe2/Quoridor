import Player
import Board

pg.init()
pg.font.init()

FONT = pg.font.Font(pg.font.get_default_font(), 10)

HEIGHT = 600
WIDTH = 800

GRAY = (50, 50, 50)
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)

win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Quoridor")
win.fill(BLACK)


def change_rect_color(rect, player, surface):
    new_rect = pg.draw.rect(surface, player.color, (rect.left,
                            rect.top, rect.width,
                            rect.height))
    return new_rect


def place_wall(player, mouse_pos, rectangle_matrix, button_clicked, board,
               surface):

    clicked_rectangle = None
    clicked_rect_row = 0
    clicked_rect_col = 0
    for row in rectangle_matrix:
        for rect in row:
            if rect.collidepoint(mouse_pos):
                clicked_rectangle = rect
                clicked_rect_row = rectangle_matrix.index(row)
                clicked_rect_col = row.index(clicked_rectangle)

    if button_clicked == "left":  # replace
        # rectangles with different coloured ones
        for n in [0, 1, 2]:
            new_rectangle = change_rect_color(rectangle_matrix
                                                   [clicked_rect_row + n]
                                                   [clicked_rect_col], player,
                                                   surface)
            print(new_rectangle)
            rectangle_matrix[clicked_rect_row + n][clicked_rect_col] = new_rectangle

    elif button_clicked == "right":
        top_left_pos = clicked_rectangle.topleft
        width = clicked_rectangle.width * 3
        height = clicked_rectangle.height
        wall = (surface, player.color, (top_left_pos[0], top_left_pos[1],
                                        width, height))
        board.list_of_walls.append(wall)

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
    run = True
    while run:

        pg.time.delay(100)
        pg.display.update()

        # create the players
        number_of_players = 2  # TODO give player choice
        players_list = Player.create_players(number_of_players)

        # draw the board
        Board.draw_board(cur_board, win)
        # draw the pieces
        Player.draw_pieces(cur_board, win)
        # draw the walls
        for w in cur_board.list_of_walls:
            pg.draw.rect(w[0], w[1], w[2])

        player_to_move = Player.get_current_player(players_list)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    move_piece(player_to_move, "north")
                elif event.key == pg.K_DOWN:
                    move_piece(player_to_move, "south")
                elif event.key == pg.K_LEFT:
                    move_piece(player_to_move, "west")
                elif event.key == pg.K_RIGHT:
                    move_piece(player_to_move, "east")
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                # left click
                click_pos = pg.mouse.get_pos()
                place_wall(player_to_move, click_pos,
                           cur_board.rectangle_matrix,
                           "left", cur_board, win)
            elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                # right click
                click_pos = pg.mouse.get_pos()
                place_wall(player_to_move, click_pos,
                           cur_board.rectangle_matrix, "right", cur_board, win)

pg.quit()
