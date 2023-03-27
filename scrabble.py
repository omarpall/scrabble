from board import Board
from bag import Bag
from player import Player

QUIT_PROMPT = 'quit'

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.players = []
        self.bag = Bag()

    def get_no_players(self):
        try:
            no_players = input("Number of players?")
            no_players = int(no_players)
            self.players = [Player() for _ in range(no_players)]
        except:
            print("That's not a number you donkey")
            self.get_no_players()

    def get_player_names(self):
        for i in range(0, len(self.players)):
            player_no = i+1
            player_name = input(f"Enter the name for Player {player_no}: ")
            self.players[i].set_name(player_name)
    
    def play_round(self):
        self.board.display_board()


    
def main():
    keep_playing = True
   
    game = Game()
    game.get_no_players()
    game.get_player_names()

    while keep_playing:
        user_input = input("yup")

        if user_input.lower() == QUIT_PROMPT:
            quit()


if __name__ == "__main__":
    main()







    