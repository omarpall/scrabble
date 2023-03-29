from PA6 import Player
import random
class Bag:
    def __init__(self) -> None:
        self.status = {'A':9, 'B':2, 'C':2, 'D':4, 'E':12, 'F':2, 'G':3, 'H':2, 'I':9, 'J':1, 'K':1, 'L':4, 'M':2, 'N':6, 'O':8, 'P':2, 'Q':1, 'R':6, 'S':4, 'T':6, 'U':4, 'V':2, 'W':2, 'X':1, 'Y':2, 'Z':1, 'Blanks':2}
        self.keys = list(self.status.keys())
        self.values = list(self.status.values())

    def draw(self, number):
        drawn = random.sample(self.keys, counts=self.values, k=number)
        for letter in drawn:
            self.status[letter] -= 1

        return drawn

    def legal_trade(self, letters, player_hand):
        player_letters = player_hand
        for letter in letters:
            if letter in player_letters:
                player_letters.remove(letter)
            else:
                return False
        return True, player_letters
    
    def trade(self,letters, player_hand):
        legal, player_letters = self.legal_trade(letters, player_hand)
        if legal == True:
            new_player_hand = self.draw(len(letters))
            for letter in player_hand:
                self.status[letter] += 1
            player_hand = player_letters + new_player_hand
        return player_hand


def main():
    b = Bag()
    trade = b.trade("BCD", ["A","B","C","D"])
    print(trade)



if __name__ == "__main__":
    main()
