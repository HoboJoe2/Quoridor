class Board:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.actual_rows = ((self.num_rows * 2) - 1)
        self.actual_cols = ((self.num_cols * 2) - 1)
        self.tile_matrix = []

    def __repr__(self):
        return f"Board({self.num_rows}, {self.num_cols})"


class Tile:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.board = board
        self.isSmall = False
        self.check_tile_size()

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
            cur_row.append(cur_tile)
        cur_board.tile_matrix.append(cur_row)
    return cur_board
