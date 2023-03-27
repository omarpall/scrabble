import numpy as np

class Board:
    def __init__(self):
        self.height = 15
        # self.letter_tile_map = np.zeros((15, 15), dtype=str)
        # self.letter_tile_map[:] = "_"
        self.letter_tile_map = [["_"] *15] * 15
        # self.width = 15
        # self.triple_word_score = [0,7,14]
        # self.double_word_score = [1,2,3,4,10,11,12,13] 
        # self.double_letter_score = [(0,3),(3,0),(0,11),(11,0),(2,6),(6,2),(7,3),(3,7),(8,2),(2,8),(6,6),(6,8),(8,6),(8,8),(14,3),(3,14),(6,12),(12,6),(7,11),(11,7),(12,8),(8,12),(11,14),(14,11)]
        # self.triple_letter_score = [(1,5),(5,1),(9,1),(1,9),(5,5),(5,9),(9,5),(13,5),(5,13),(9,9),(9,13),(13,9)]
        # self.start = (7,7)

    def init_bonus_tile_map(self):
        pass

    def set_letter(self, tile, letter):
        self.letter_tile_map[tile.x][tile.y] = letter

    def display_board(self):
        print(self.letter_tile_map)

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def main():
    b = Board()
    b.set_letter(Tile(0,5), 'A')
    b.print_board()



if __name__ == "__main__":
    main()