class Board:
    def __init__(self) -> None:
        self.height = 15
        self.width = 15
        self.triple_word_score = [0,7,14]
        self.double_word_score = [1,2,3,4,10,11,12,13] 
        self.double_letter_score = [(0,3),(3,0),(0,11),(11,0),(2,6),(6,2),(7,3),(3,7),(8,2),(2,8),(6,6),(6,8),(8,6),(8,8),(14,3),(3,14),(6,12),(12,6),(7,11),(11,7),(12,8),(8,12),(11,14),(14,11)]
        self.triple_letter_score = [(1,5),(5,1),(9,1),(1,9),(5,5),(5,9),(9,5),(13,5),(5,13),(9,9),(9,13),(13,9)]
        self.start = (7,7)

    def create_bonus_tile_map(self):
        bonus_map = np.zeros(15, 15)
        for index in self.triple_word_score:
            bonus_map[index][index] = (3, 'word')
            def triple_word(self, word_pionts):
                word_pionts *= 3
                return word_pionts
