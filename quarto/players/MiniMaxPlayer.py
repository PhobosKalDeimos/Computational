import random
from quarto.objects import Player, Quarto
from copy import deepcopy
import numpy as np

class MiniMaxPlayer(Player):
    """MiniMax player"""

    def __init__(self, quarto: Quarto) -> None:
        super().__init__(quarto)
        self.maximizing= False
        self.threshold_min_max= 10
 
    def choose_piece(self) -> int:
        game= self.get_game()
        board = self.get_game().get_board_status()
        available_pieces = [piece for piece in range(self.get_game().BOARD_SIDE**2) if piece not in board]
        #use the same strategy as in hard coded player
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
        num_free= np.count_nonzero(board == -1)

        if num_free<= self.threshold_min_max:
            p= game.get_current_player()
            if p==0:
                self.maximizing = False
            else:
                self.maximizing= True
            (i, j), _= minmax(game, self.maximizing)
            return (i, j)
        else:
            #use the same strategy as in hard coded player
            for j in range(game.BOARD_SIDE):
                for i in range(game.BOARD_SIDE):
                    p= board[j, i] # the value of the (j,i) position on the board
                    if p== -1: # free position
                        tmp= deepcopy(game)
                        tmp.place(i, j) # place the selected element in the (j, i) position; "swapped" because of the functions place and placeable in objects.py"
                        if check_winnable(tmp): 
                            return (i, j) # "swapped" because of the functions place and placeable in objects.py"
            return (random.randint(0, 3), random.randint(0, 3))




def eval_state(game) -> int:
    if not game.check_finished() and game.check_winner()< 0:
        return 0
    else:
        if game.check_winner()== 0: 
            return 1 
        else: 
            return -1 

def minmax(game, maximizing, alpha= -1, beta= 1) -> tuple[tuple[int, int], int]:
    val= eval_state(game)
    if val!= 0:
        return None, val
    board_status= game.get_board_status()
    best_place= ()
    if maximizing:
        best= -1
        for j in range(game.BOARD_SIDE):
            for i in range(game.BOARD_SIDE):
                p= board_status[j, i] 
                if p== -1: # free position
                    tmp= deepcopy(game)
                    tmp.place(i, j)
                    _, val= minmax(tmp, maximizing, alpha, beta)
                    if best<= -val:
                        best_place= (i, j)
                        best= -val
                    alpha= max(alpha, best)
                    if beta<= alpha: #pruning
                        break
        return  best_place, best
    else:
        best= 1
        for j in range(game.BOARD_SIDE):
            for i in range(game.BOARD_SIDE):
                p= board_status[j, i]
                if p== -1: # free position
                    tmp= deepcopy(game)
                    tmp.place(i, j)
                    _, val= minmax(tmp, maximizing, alpha, beta)
                    if best>= -val:
                        best_place= (i, j)
                        best= -val
                    beta= min(beta, best)
                    if beta<= alpha: #pruning
                        break
        return best_place, best    






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

