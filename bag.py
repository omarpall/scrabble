import random
class Bag:
    def __init__(self) -> None:
        self.status = {'A':9, 'B':2, 'C':2, 'D':4, 'E':12, 'F':2, 'G':3, 'H':2, 'I':9, 'J':1, 'K':1, 'L':4, 'M':2, 'N':6, 'O':8, 'P':2, 'Q':1, 'R':6, 'S':4, 'T':6, 'U':4, 'V':2, 'W':2, 'X':1, 'Y':2, 'Z':1, 'Blanks':2}

    def draw_tiles(self, no_tiles):
        keys = list(self.status.keys())
        values = list(self.status.values())
        drawn_tiles = random.sample(keys, counts=values, k=no_tiles)

