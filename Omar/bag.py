import random
from rich.console import Console
console = Console()

class Bag:
    def __init__(self) -> None:
        self.status = {'A':9, 'B':2, 'C':2, 'D':4, 'E':12, 'F':2, 'G':3, 'H':2, 'I':9, 'J':1, 'K':1, 'L':4, 'M':2, 'N':6, 'O':8, 'P':2, 'Q':1, 'R':6, 'S':4, 'T':6, 'U':4, 'V':2, 'W':2, 'X':1, 'Y':2, 'Z':1}#, 'BLANK':2}


    def draw_letters(self, no_letters):
        keys = list(self.status.keys())
        values = list(self.status.values())
        drawn_no_letters = min(self.get_no_letters_in_bag(), no_letters)
        drawn_letters = []
        if drawn_no_letters > 0:
            drawn_letters = random.sample(keys, counts=values, k=drawn_no_letters)

        for letter in drawn_letters:
            self.status[letter] -= 1
        return drawn_letters

    def put_letters_in_bag(self, letters):
        for letter in letters:
            self.status[letter] += 1

    def get_no_letters_in_bag(self):
        return sum(list(self.status.values()))

    def is_empty(self):
        for value in self.status.values():
            if value != 0:
                return False
        return True



def main():
    b = Bag()
    trade = b.trade("ABCD", ["A","B","C","D"])
    print(trade)



if __name__ == "__main__":
    main()