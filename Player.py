class Player:
    def __init__(self, color, goes_first, x, y):
        self.color = color
        self.walls_left = 10
        self.is_their_turn = goes_first
        self.piece_xy = {"x": x, "y": y}
        self.legal_moves = {"north": True, "south": True, "east": True, "west": True}

    def __repr__(self):
        return f"Player({self.color}, {self.is_their_turn}, {self.piece_xy})"
