import pygame as pg

HEIGHT = 600
WIDTH = 800

GRAY = (50, 50, 50)
WHITE = (200, 200, 200)


class Board:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.actual_rows = ((self.num_rows * 2) - 1)
        self.actual_cols = ((self.num_cols * 2) - 1)
        self.tile_matrix = []
        self.rectangle_matrix = []
        self.list_of_walls = []

    def __repr__(self):
        return f"Board({self.num_rows}, {self.num_cols})"


class Tile:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board
        self.isSmall = False

    def check_tile_size(self):
        if self.x % 2 != 0 or self.y % 2 != 0:  # check if row is odd
            self.isSmall = True
            return
        else:
            self.isSmall = False
            return


def create_board(rows, columns):
    cur_board = Board(rows, columns)
    for row in range(cur_board.actual_rows):
        cur_row = []
        for col in range(cur_board.actual_cols):
            cur_tile = Tile(row, col, cur_board)
            cur_tile.check_tile_size()
            cur_row.append(cur_tile)
        cur_board.tile_matrix.append(cur_row)
    return cur_board


def draw_board(board, surface):
    tile_width = (WIDTH / board.actual_cols)
    tile_height = (HEIGHT / board.actual_rows)

    if board.rectangle_matrix == []:
        for row in board.tile_matrix:
            cur_row = []
            for tile in row:
                x_pos = tile_width * tile.y
                y_pos = tile_height * tile.x
                if tile.isSmall:
                    color = GRAY
                else:
                    color = WHITE

                new_rect = pg.draw.rect(surface,
                                        color, (int(x_pos), int(y_pos),
                                                int(tile_width),
                                                int(tile_height)))
                cur_row.append(new_rect)
            board.rectangle_matrix.append(cur_row)
    return
