import numpy as np
from rich.console import Console
console = Console()
ERROR_STYLE = 'red b'

class Board:


    def __init__(self):
        self.size = 15
        self.letter_tile_map = [[Tile(x=i, y=j) for i in range(self.size)] for j in range(self.size)]
        self.letter_tile_map[7][7].legal = True
        self.letter_scores = {'A':1, 'B':3, 'C':3, 'D':2, 'E':1, 'F':4, 'G':2, 'H':4, 'I':1, 'J':8, 'K':5, 'L':4, 'M':3, 'N':1, 'O':8, 'P':2, 'Q':10, 'R':1, 'S':1, 'T':1, 'U':1, 'V':4, 'W':4, 'X':8, 'Y':4, 'Z':10}
        
        self.init_bonus_tiles()

    def init_bonus_tiles(self):
        triple_word_score = [0,7,14]
        double_word_score = [1,2,3,4] 
        double_letter_score = [(0,3),(3,0),(0,11),(11,0),(2,6),(6,2),(7,3),(3,7),(8,2),(2,8),(6,6),(6,8),(8,6),(8,8),(14,3),(3,14),(6,12),(12,6),(7,11),(11,7),(12,8),(8,12),(11,14),(14,11)]
        triple_letter_score = [(1,5),(5,1),(9,1),(1,9),(5,5),(5,9),(9,5),(13,5),(5,13),(9,9),(9,13),(13,9)]
        
        for index in triple_word_score:
            for index2 in triple_word_score:  
                self.letter_tile_map[index][index2].set_bonus_tile('3', 'w')
        self.letter_tile_map[7][7].set_bonus_tile('', '') #starting tile in middle

        for index in double_word_score:
            self.letter_tile_map[index][index].set_bonus_tile('2', 'w')
            self.letter_tile_map[index][self.size-index-1].set_bonus_tile('2', 'w')
            self.letter_tile_map[self.size-index-1][index].set_bonus_tile('2', 'w')
            self.letter_tile_map[self.size-index-1][self.size-index-1].set_bonus_tile('2', 'w')
            
        for coordinate in double_letter_score:
            self.letter_tile_map[coordinate[0]][coordinate[1]].set_bonus_tile('2', 'l')

        for coordinate in triple_letter_score:
            self.letter_tile_map[coordinate[0]][coordinate[1]].set_bonus_tile('3', 'l')


    def get_tile_in_pos(self, pos):
        if pos[0] > 0 and pos[0] < self.size and pos[1] > 0 and pos[1] < self.size:
            return self.letter_tile_map[pos[1]][pos[0]]
        else:
            return Tile(-1, -1)
    
    def is_letter_around_word(self, place_action_object):
        start_x = place_action_object.x
        start_y = place_action_object.y
        end_x = place_action_object.end_pos[0]
        end_y = place_action_object.end_pos[1]
        direction = place_action_object.direction
        if direction == 'H':
            left_letter_pos = (start_x - 1, start_y)
            left_letter = self.get_tile_in_pos(left_letter_pos)
            right_letter_pos = (end_x + 1, start_y)
            right_letter = self.get_tile_in_pos(right_letter_pos)  
            if (not left_letter or not left_letter.letter) and (not right_letter or not right_letter.letter):
                return False
            return True
        elif direction == 'V':
            top_letter_pos = (start_x, start_y - 1)
            top_letter = self.get_tile_in_pos(top_letter_pos)
            bottom_letter_pos = (start_x , end_y + 1)
            bottom_letter = self.get_tile_in_pos(bottom_letter_pos)
            if (not top_letter or not top_letter.letter) and (not bottom_letter or not bottom_letter.letter):
                return False
            return True

    def check_for_adjacent_letter(self, x, y, direction):
        if direction == 'H':
            letter_above = self.get_tile_in_pos(pos = (x,y-1)).letter
            letter_under = self.get_tile_in_pos(pos = (x,y+1)).letter
            if letter_above or letter_under:
                return True   
        elif direction == 'V':
            letter_left = self.get_tile_in_pos(pos = (x-1,y)).letter
            letter_right = self.get_tile_in_pos(pos = (x+1,y)).letter
            if letter_left or letter_right:
                return True
        return False

   
    def is_place_action_legal(self, place_action_object, hand):
        tmp_hand = hand.copy()
        touching_legal_tile = False
        if self.is_letter_around_word(place_action_object):
            console.print('The word is longer on the board', style=ERROR_STYLE)
            return False
      
        x = place_action_object.get_x()
        y = place_action_object.get_y()
        direction = place_action_object.get_direction()
        word = place_action_object.get_word()

        
        for letter in word:
            tile = self.letter_tile_map[y][x] 
            if tile.legal or self.check_for_adjacent_letter(x, y, direction):
                touching_legal_tile = True
            if  x > self.size-1 or  y > self.size-1:
                console.print('Out of bounds', style=ERROR_STYLE)
                return False
            if tile.letter:
                if letter != tile.letter:
                    console.print('Letter on board in the way', style=ERROR_STYLE)
                    return False
            else:
                if letter in hand:
                    tmp_hand.remove(letter)
                else:
                    console.print(f'Letter {letter} not in hand', style=ERROR_STYLE)
                    return False
            
            if direction == 'H':
                x += 1
            elif direction == 'V':
                y += 1
    
        if not touching_legal_tile:
            console.print('Invalid position on board', style=ERROR_STYLE)
            return False
        return True 


    def place_letters(self, place_action_object, hand):
        is_legal = self.is_place_action_legal(place_action_object, hand)
        score = 0
        score_mult = 1
        if not is_legal:
            return (False, score)
      
        x = place_action_object.get_x()
        y = place_action_object.get_y()
        direction = place_action_object.get_direction()
        word = place_action_object.get_word()
        
        for letter in word:
            tile = self.letter_tile_map[y][x]
            letter_score = self.letter_scores[letter]
            letter_mult = 1

            if not tile.letter:
                
                hand.remove(letter)
                if tile.bonus_tile_mult:
                    if tile.bonus_tile_type == 'l':
                        letter_mult = int(tile.bonus_tile_mult)
                    elif tile.bonus_tile_type == 'w':
                        score_mult = int(tile.bonus_tile_mult)
                tile.set_letter(letter)
            score += letter_mult * letter_score

            if direction == 'H':
                x += 1
            elif direction == 'V':
                y += 1
        score *= score_mult
        if hand == []:
            score += 50
        return (True, score)
        

    def set_letter(self, tile, letter):
        self.letter_tile_map[tile.x][tile.y] = letter

    def display_board(self):
        console.print( "Current board state:", style='b u magenta ')

        for i in range(self.size):
            if i >= 10:
                console.print(i, end=' ')
            else:
                console.print(i, end='  ')
            for j in range(self.size):
                tile = self.letter_tile_map[i][j]
                style = tile.get_style()
                if tile.letter:
                    end = '  '
                else:
                    end = ' '
                console.print(tile, style=style, end=end)
            print()

        console.print('   ', end='')
        for k in range(self.size):
            if k >= 10:
                console.print(k, end=' ')
            else:
                console.print(k, end='  ')
        print()
        print()


class Tile:
    style_guide = {('2', 'l'): '#637FAA', ('3', 'l'): '#225A95',('2', 'w'): '#B08930',('3', 'w'): '#9A111F'}
    letter = ''
    bonus_tile_mult = ''
    bonus_tile_type = ''
    mult_combo = None
    legal = False
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_bonus_tile(self, bonus_tile_mult, bonus_tile_type):
        self.bonus_tile_mult = bonus_tile_mult
        self.bonus_tile_type = bonus_tile_type
        self.mult_combo = (bonus_tile_mult, bonus_tile_type)

    def set_letter(self, letter):
        self.letter = letter
        self.legal = True
        self.set_bonus_tile('', '')

    def get_style(self):
        if self.bonus_tile_mult and self.bonus_tile_type:
            return self.style_guide[self.mult_combo]
        else:
            return 'white b'
        
    def __str__(self):
        if self.letter:
            return self.letter
        elif self.bonus_tile_mult and self.bonus_tile_type:
            return str(self.bonus_tile_mult) + self.bonus_tile_type
        else:
            return '__'
