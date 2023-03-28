class PlaceAction:


    def __init__(self, word, start_pos, direction):
        self.word = word.upper()
        self.start_pos = start_pos
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.direction = direction.upper()
        self.length = len(word)
        if self.direction == 'H':
            self.end_pos = (int(self.x) + self.length-1, int(self.y))
        elif self.direction == 'V':
            self.end_pos = (int(self.x), int(self.y) + self.length-1)


    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_direction(self):
        return self.direction
    def get_word(self):
        return self.word