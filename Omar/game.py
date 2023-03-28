from board import Board
from board import Tile
from bag import Bag
from player import Player
from place_action import PlaceAction
import time
from rich.console import Console
console = Console()


QUIT_PROMPT = 'quit'
SETUP_STYLE = 'color(2) b'
SUCCESS_STYLE = 'green b'
ACTION_STYLE = 'magenta b'
ERROR_STYLE = 'red b'
ACTIONS = {'1':'Place', '2':'Trade', '3':'Pass'}



class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.bag = Bag()
        self.players = []
        self.current_player = None
        self.pass_counter = 0
        self.wordlist = []
        with open("Collins Scrabble Words (2019) with definitions-1.txt", 'r') as f:
            next(f)
            next(f)
            self.wordlist = [line.split("\t")[0] for line in f]



    def get_no_players(self):
        try:
            console.print(f"Number of players?" , style=SETUP_STYLE, end= ' ')
            no_players = input()
            no_players = int(no_players)
            if no_players < 2 or no_players > 4:
                self.get_no_players()
            self.no_players = no_players
            self.players = [Player() for _ in range(no_players)]
            
        except:
            console.print("Players need to be between 2-4", style=ERROR_STYLE)
            self.get_no_players()

    def does_word_exist(self, word):
        if word in self.wordlist:
            return True
        return False

    def get_player_names(self):
        for i in range(0, len(self.players)):
            player_no = i+1
            console.print(f"Enter the name for Player {player_no}: " , style=SETUP_STYLE, end= ' ')
            player_name = input()#player_name = "Player " + str(i+1)#
            self.players[i].set_name(player_name)
        self.current_player = self.players[0]

    
    def count_hand_score(self, hand):
        letter_scores = self.board.letter_scores
        hand_score = 0
        for letter in hand:
            hand_score += letter_scores[letter]
        return hand_score

    def check_if_game_over(self):
        if self.bag.is_empty() and self.current_player.hand == []:
            for player in self.players:
                if player != self.current_player:
                    hand_score = self.count_hand_score(player.hand)
                    player.score -= hand_score
                    self.current_player.score += hand_score
            return True
        return False

    def play_round(self):
        for player in self.players:
            self.current_player = player
            player.draw_letters(self.bag)
            self.board.display_board()
            time.sleep(1)
            self.current_player.display_hand()
            time.sleep(0.8)
            self.perform_action_sequence()
            if self.check_if_game_over():
                return False
        if self.pass_counter >= self.no_players*2:
            return False
        return True
            
    def get_place_action_object(self,place_action_str):
        try:
            word, coord, direction = place_action_str.split(' ')
        except:
            return None
        x, y = coord.split(',')
        x, y = int(x), int(y)
        start_pos = (x,y)
        if direction.upper() not in ('HV'):
            console.print('The direction needs to be H or V', style=ERROR_STYLE)
            return None
        if x < 0 or x > self.board.size-1 or y < 0 or y > self.board.size-1:
            console.print(f'{x}, {y} is out of bounds', style=ERROR_STYLE)
            return None
        place_action_object = PlaceAction(word.upper(), start_pos, direction.upper())
        return place_action_object

    def perform_place_action(self, place_action_object):
        placed_letters, placed_letters_score = self.board.place_letters(place_action_object, self.current_player.hand)
        self.current_player.score += placed_letters_score
        return placed_letters, placed_letters_score




    def perform_trade_action(self,letters):
        legal_trade = self.current_player.is_trade_legal(letters)
        if not legal_trade:
            return False
        self.current_player.trade(letters, self.bag)
        return True
        
    def place_prompt(self):
        console.print(f"Type the word, coordinates(x, y) and direction(H or V) (Horizontal or Vertical)" , style=ACTION_STYLE)
        console.print(f"For example: ", style=ACTION_STYLE, end='')
        console.print(f"[green b]CAT 7,7 H[/green b]")
        place_action_str = input()
        place_action_object = self.get_place_action_object(place_action_str)
        if not place_action_object:
            console.print(f"Invalid format, try again", style=ERROR_STYLE)
            self.place_prompt()
        else:
            if not self.does_word_exist(place_action_object.word):
                console.print(f"Word {place_action_object.word} doesn't exist", style=ERROR_STYLE)
                time.sleep(2)
            else:
                placed_letters, placed_score = self.perform_place_action(place_action_object)
                if not placed_letters:
                    console.print(f"That move is not legal", style=ERROR_STYLE)
                    print()
                    time.sleep(2)
                    self.perform_action_sequence()
                else:
                    console.print(f"Legal move: placing on board [yellow]Score for move: {placed_score}[/yellow]", style=SUCCESS_STYLE)
                    time.sleep(2)
                    self.pass_counter = 0

    def trade_prompt(self):
        console.print(f"What tiles would you like to trade?" , style=ACTION_STYLE)
        console.print(f"For example: ", style=ACTION_STYLE, end='')
        console.print(f"ABC", style='green b')
        letters = input().upper()
        performed_trade_action = self.perform_trade_action(letters)       
        if not performed_trade_action:
            console.print(f"You don't have those letters", style=ERROR_STYLE)
            self.trade_prompt()
        else:
            print()
            console.print(f"Success: Trading letters [red]{letters}[/red]", style=SUCCESS_STYLE)
            self.current_player.display_hand()
            time.sleep(2)
            self.pass_counter = 0

    def perform_action_sequence(self):       
        action = self.get_action()
        if action in ('1', '2', '3'):
            action_str = ACTIONS[action]
            if action_str == 'Place':

                self.place_prompt()
            if action_str == 'Trade':
                self.trade_prompt()
            if action_str == 'Pass':
                self.pass_counter += 1
        else:
            console.print(f"Choose action 1, 2 or 3", style=ERROR_STYLE)
            self.perform_action_sequence()

    def get_action(self):
        console.print(f"Player ", style=ACTION_STYLE, end='')
        console.print(self.current_player.name, style="yellow b", end=' ')
        console.print(f"choose an action" , style=ACTION_STYLE)
        console.print(f"[1] Place tiles" , style=ACTION_STYLE)
        console.print(f"[2] Trade tiles" , style=ACTION_STYLE)
        console.print(f"[3] Pass" , style=ACTION_STYLE)
        action = input()
        if action.lower() == QUIT_PROMPT:
            quit()
        return action


    def show_scores(self):
        players_in_order = sorted(self.players, key=lambda x: x.score, reverse=True)
        winner = players_in_order[0]
        console.print(f"The winner is: [yellow]{winner.name}[/yellow]" , style=SUCCESS_STYLE)
        print()
        places = ['1st', '2nd', '3rd', '4th']
        for index, player in enumerate(players_in_order):
            place = places[index]
            console.print(f"{place}: [yellow]{player.name}[/yellow] with a score of [yellow]{player.score}[/yellow]" , style=SUCCESS_STYLE)

def main():
    game = Game()
    game.get_no_players()
    game.get_player_names()
    game.show_scores()


if __name__ == "__main__":
    main()




    