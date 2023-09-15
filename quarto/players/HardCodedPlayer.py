import random
from quarto.objects import Player, Quarto
from copy import deepcopy
import numpy as np


class HardCodedPlayer(Player):
    """Player using coded rules"""
    def __init__(self, quarto: Quarto) -> None:
        super().__init__(quarto)
    
    def choose_piece(self) -> int:
        game= self.get_game()
        board = self.get_game().get_board_status()
        available_pieces = [piece for piece in range(self.get_game().BOARD_SIDE**2) if piece not in board]

        for p in available_pieces:
            for j in range(game.BOARD_SIDE):
                for i in range(game.BOARD_SIDE):
                    pos= board[j, i] # the value of the (j,i) position on the board
                    if pos== -1: 
                        tmp= deepcopy(game)
                        tmp.select(p) # select an element from the not placed yet list
                        tmp.place(i, j) # place the selected element in the (j, i) position; "swapped" because of the functions place and placeable in objects.py"
                        if(not check_winnable(tmp)):
                            return p
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        game= self.get_game()
        board= game.get_board_status()
        for j in range(game.BOARD_SIDE):
            for i in range(game.BOARD_SIDE):
                p= board[j, i] # the value of the (j,i) position on the board
                if p== -1: # free position
                    tmp= deepcopy(game)
                    tmp.place(i, j) # place the selected element in the (j, i) position; "swapped" because of the functions place and placeable in objects.py"
                    if check_winnable(tmp): 
                        return (i, j) # "swapped" because of the functions place and placeable in objects.py"
        return (random.randint(0, 3), random.randint(0, 3))

def check_winnable(game) -> bool:
    return (check_horizontal(game) %2 == 0 or check_vertical(game) %2 == 0 or check_diag1(game)  %2 == 0 or check_diag2(game)  %2 == 0)


def check_horizontal(game):
    board= game.get_board_status()
    for i in range(game.BOARD_SIDE):
        vals = np.where(board[i, :] > -1)[0]
        for type in range(4):
            for val in range(2):
                l= np.count_nonzero((vals>>type)&1 == val)

                for len in range(game.BOARD_SIDE):
                    if l == game.BOARD_SIDE - len:
                        return game.BOARD_SIDE - len
                
    return 0

def check_vertical(game):
    board= game.get_board_status()
    for i in range(game.BOARD_SIDE):
        vals = np.where(board[:, i] > -1)[0]
        for type in range(4):
            for val in range(2):
                l= np.count_nonzero((vals>>type)&1 == val)

                for len in range(game.BOARD_SIDE):
                    if l == game.BOARD_SIDE - len:
                        return game.BOARD_SIDE - len
                
    return 0


def check_diag1(game):
    board= game.get_board_status()
    vals = np.where(np.diag(board) == -1)[0]
    for type in range(4):
        for val in range(2):
            l= np.count_nonzero((vals>>type)&1 == val)

            for len in range(game.BOARD_SIDE):
                if l == game.BOARD_SIDE - len:
                    return game.BOARD_SIDE - len
                
    return 0


def check_diag2(game):
    board= game.get_board_status()
    vals = np.where(np.diag(np.fliplr(board)) == -1)[0]
    for type in range(4):
        for val in range(2):
            l= np.count_nonzero((vals>>type)&1 == val)

            for len in range(game.BOARD_SIDE):
                if l == game.BOARD_SIDE - len:
                    return game.BOARD_SIDE - len
                
    return 0



