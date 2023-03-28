from rich.console import Console
console = Console()

class Player:

    def __init__(self):
        self.score = 0
        self.hand = []
        self.name = ""
        self.MAX_HAND = 7

    def set_name(self, name):
        self.name = name

    def place_word(self, letters, starting_tile, direction):
        pass

    def draw_letters(self, bag):
        no_letters_to_draw = self.MAX_HAND - len(self.hand)
        drawn_letters = bag.draw_letters(no_letters_to_draw)
        self.hand += (drawn_letters)

    def display_hand(self):
        console.print(f"Player [yellow]{self.name}[/yellow] letters: {self.hand}  [yellow]Score = {self.score}[/yellow]", style='blue b')

        print()

    def is_trade_legal(self, letters):
        tmp_hand = self.hand.copy()
        for letter in letters:

            if letter in self.hand:
                tmp_hand.remove(letter)
            else:
                return False
        return True

    def trade(self, letters, bag):
        no_letters = len(letters)
        new_letters = bag.draw_letters(no_letters)
        for letter in letters:
            self.hand.remove(letter)
        self.hand += new_letters