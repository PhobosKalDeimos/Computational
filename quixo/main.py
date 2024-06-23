import random
import math
from copy import deepcopy
import numpy as np
from game import Game, Move, Player
from tqdm import tqdm

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move
    

 
class Node():
    def __init__(self, player, move=[None, None, None], depth=0, children=None) -> None:
        if player == 1:
            self.eval = -math.inf
        else:
            self.eval = math.inf
        self.move = move
        self.depth = depth
        if children == None:
            self.children = []
        else:
            self.children = children
        self.alpha = -math.inf
        self.beta = math.inf

    def get_fitness(self) -> int:
        return self.eval
    
    def add_children(self, child):
        self.children.append(child)
    
    def print_tree(self):
        print(f"Node {self.depth}: {self.move} | eval = {self.eval} | children: {len(self.children)}")
        for c in self.children:
            c.print_tree()

class MinmaxPlayer(Player):
    def __init__(self, depth) -> None:
        super().__init__()
        self.depth = depth

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        computed_move = self.simulate_move(game)
        from_pos = (computed_move[0], computed_move[1])
        move = computed_move[2]
        return from_pos, move
    
    def simulate_move(self, game: 'Game'):
        tree = Node(game.get_current_player())
        best_reward, best_node = self.minmax(game, tree, True, game.get_current_player())
        tree.eval = best_reward
        tree.move = best_node.move
        return tree.move
    
    def minmax(self, game, parent, maximizing_player, player_id, alpha=-math.inf, beta=math.inf):
        current_player = game.get_current_player()
        #check end
        if parent.depth == self.depth or game.check_winner() > -1:
            reward = self.fitness(game.check_winner(), game.get_board(), player_id)
            return reward, None

        if maximizing_player:
            max_eval = -math.inf
            best_node = None
            # iterate all possible moves
            for col in range(5):
                for row in range(5):
                    possible_moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
                    for move in possible_moves:
                        game_copy = deepcopy(game)
                        if game_copy.move(col, row, move, current_player):  # make move if allowed
                            node = Node(current_player, [col, row, move], parent.depth+1)   
                            parent.add_children(node)
                            game_copy.switch_player()    #switch player before call recoursive function
                            eval, _ = self.minmax(game_copy, node, False, player_id, alpha, beta)
                            node.eval = eval
                            if (eval > max_eval):
                                max_eval = eval
                                best_node = node
                            alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break
            return max_eval, best_node
        else:
            min_eval = math.inf
            best_node = None
            # iterate all possible moves
            for col in range(5):
                for row in range(5):
                    possible_moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
                    for move in possible_moves:
                        game_copy = deepcopy(game)
                        if game_copy.move(col, row, move, current_player):  # make move if allowed
                            node = Node(current_player, [col, row, move], parent.depth+1)
                            parent.add_children(node)
                            game_copy.switch_player()    #switch player before call recoursive function
                            eval, _ = self.minmax(game_copy, node, True, player_id, alpha, beta)
                            node.eval = eval
                            if (eval < min_eval):
                                min_eval = eval
                                best_node = node
                            beta = min(beta, eval)
                        if beta <= alpha:
                            break
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break
            return min_eval, best_node

    def fitness (self, is_winner, board, player_id):
        #count zeros and ones on rows, column and diagonals
        consecutive_one = sum(np.count_nonzero(board == 1, axis=0) + np.count_nonzero(board == 1, axis=1)) + np.count_nonzero(np.diagonal(board) == 1) + np.count_nonzero(np.diagonal(np.flip(board, axis=1)) == 1)
        consecutive_zero = sum(np.count_nonzero(board == 0, axis=0) + np.count_nonzero(board == 0, axis=1)) + np.count_nonzero(np.diagonal(board) == 0) + np.count_nonzero(np.diagonal(np.flip(board, axis=1)) == 0)    
        
        #compute reward in case of no winner player
        if player_id == 0 :
            reward = (consecutive_zero - consecutive_one)
        else:
            reward = -(consecutive_zero - consecutive_one)
        
        #if minmax player wins set maximum reward else set mximum penalty
        if is_winner == player_id:
            reward = math.inf
        elif is_winner > -1 :
            reward = -math.inf
        
        return reward


    
def play_games(player1, player2, num_of_games):
    p0_wins = 0
    p1_wins = 0
    for _ in tqdm(range(num_of_games)):
        game = Game()
        winner = game.play(player1, player2)
        if winner:
            p1_wins += 1
        else:
            p0_wins += 1
    print (f"P0 wins: {p0_wins}, P1 wins: {p1_wins}\n")



if __name__ == '__main__':
    random_player = RandomPlayer()
    minmax_player_1 = MinmaxPlayer(1)
    minmax_player_2 = MinmaxPlayer(2)


    num_of_games = 100

    print (f"Player 0: Random Player vs Player 1: MinMax Player (with depth=1) | {num_of_games} games")
    play_games(random_player, minmax_player_1, num_of_games)

    print (f"Player 0: Random Player vs Player 1: MinMax Player (with depth=2) | {num_of_games} games")
    play_games(random_player, minmax_player_2, num_of_games)

    print (f"Player 0: MinMax Player (with depth=2) vs Player 1: MinMax Player (with depth=1) | {num_of_games} games")
    play_games(minmax_player_2, minmax_player_1, num_of_games)




