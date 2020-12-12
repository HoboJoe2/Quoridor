import pygame as pg
import Player
import Board

# testing git commit

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


def place_wall(player, mouse_pos, rectangle_sprites, button_clicked, board,
               surface):
    clicked_sprites = [r for r in rectangle_sprites if
                       r.collidepoint(mouse_pos)]

    if button_clicked == "left":
        top_left_pos = clicked_sprites[0].topleft
        width = clicked_sprites[0].width
        height = clicked_sprites[0].height * 3
        wall = (surface, player.color, (top_left_pos[0], top_left_pos[1],
                                        width, height))
        board.list_of_walls.append(wall)
    elif button_clicked == "right":
        top_left_pos = clicked_sprites[0].topleft
        width = clicked_sprites[0].width * 3
        height = clicked_sprites[0].height
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


def draw_board(board, surface):
    tile_width = (WIDTH / board.actual_cols)
    tile_height = (HEIGHT / board.actual_rows)
    square_dimensions = {"width": tile_width, "height": tile_height}
    rects = []

    for tile in board.board_matrix:
        x_pos = tile_width * tile.y
        y_pos = tile_height * tile.x
        if tile.isSmall:
            color = GRAY
        else:
            color = WHITE

        new_rect = pg.draw.rect(surface,
                                color, (int(x_pos), int(y_pos),
                                        int(tile_width), int(tile_height)))
        rects.append(new_rect)
    return square_dimensions, rects


# draw the board and get the dimensions
# (in order to draw the pieces and walls)
cur_board = Board.create_board(9, 9)
tile_dimensions, rectangles = draw_board(cur_board, win)

if __name__ == "__main__":
    run = True
    while run:

        pg.time.delay(100)
        pg.display.update()

        # create the players
        number_of_players = 2  # TODO give player choice
        players_list = Player.create_players(number_of_players)

        # draw the board

        # draw the pieces

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
                place_wall(player_to_move, click_pos, rectangles,
                           "left", cur_board, win)
            elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                # right click
                click_pos = pg.mouse.get_pos()
                place_wall(player_to_move, click_pos,
                           rectangles, "right", cur_board, win)

pg.quit()
