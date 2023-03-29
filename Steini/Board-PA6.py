class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    

class Board:
    def __init__(self) -> None:
        self.height = 15
        self.width = 15
        self.triple_word_score = [(0,0),(0,7),(0,14),(7,0),(7,14),(14,0),(14,7),(14,14)]
        self.double_word_score = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(13,1), (12,2), (11,3), (10,4), (9,5), (8,6), (6,8), (5,9), (4,10), (3,11), (2,12), (1,13)]
        self.triple_letter_score = [(1,5),(5,1),(9,1),(1,9),(5,5),(5,9),(9,5),(13,5),(5,13),(9,9),(9,13),(13,9)]
        self.double_letter_score = [(0,3),(3,0),(0,11),(11,0),(2,6),(6,2),(7,3),(3,7),(8,2),(2,8),(6,6),(6,8),(8,6),(8,8),(14,3),(3,14),(6,12),(12,6),(7,11),(11,7),(12,8),(8,12),(11,14),(14,11)]
        self.start = (7,7)
        self.placed_letters = {}

    def create_bonus_tile_map(self):
        ret_string = ""
        for i in range(self.height):
            for j in range(self.width):
                point = (i,j)
                if str(point) in self.placed_letters.keys():
                    ret_string += f"│{self.placed_letters[str(point)]}_"
                elif (i,j) in self.triple_word_score:
                    ret_string += "│3W"
                elif (i,j) in self.double_word_score:
                    ret_string += "│2W"
                elif (i,j) == self.start:
                    ret_string += "│★_"
                elif (i,j) in self.triple_letter_score:
                    ret_string += "│3L"
                elif (i,j) in self.double_letter_score:
                    ret_string += "│2L"
                else:
                    ret_string += "│__"
            ret_string += "│\n"

        return ret_string
    
    def place_word(self,point, direction, word):
        point = Position(point[0], point[1])

        if direction == "D":
            for letter in word:
                self.placed_letters[str(point)] = letter
                point += Position(1,0)

        if direction == "R":
            for letter in word:
                self.placed_letters[str(point)] = letter
                point += Position(0,1)


       

def main():
    b = Board()
    board = b.create_bonus_tile_map()
    print(board)

    start_point = (7,7)
    b.place_word(start_point,"R","HELLO")
    print(b.placed_letters)

    board2 = b.create_bonus_tile_map()

    print(board2)



if __name__ == "__main__":
    main()
