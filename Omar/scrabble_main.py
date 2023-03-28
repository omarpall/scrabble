from game import Game
from rich.console import Console
import time
console = Console()

def main():
    

    keep_playing = True
   
    game = Game()
    game.get_no_players()
    game.get_player_names()
    console.print("-------------- STARTING GAME --------------", style=' b')
    time.sleep(0.5)
    while keep_playing:
        keep_playing = game.play_round()
    game.show_scores()


if __name__ == "__main__":
    main()
