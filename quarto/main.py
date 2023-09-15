# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
import random
import quarto
from tqdm import tqdm

from players.RandomPlayer import RandomPlayer
from players.HardCodedPlayer import HardCodedPlayer
from players.MiniMaxPlayer import MiniMaxPlayer


NUM_OF_EVALUATIONS = 10


def evaluate(game: quarto.Quarto, p1: quarto.Player, p2: quarto.Player, num_games: int= NUM_OF_EVALUATIONS) -> None:
    
    wins = 0
    tieds = 0
    losses = 0
    
    for n in tqdm(range(num_games)):
        game.reset()
        game.set_players((p1, p2))
        res = game.run(verbose=False)
        if res==0: wins+=1
        if res==1: losses+=1
        if res==-1: tieds+=1

    print(f"Player1: wins {wins} ({wins/num_games}) | tiedes {tieds} ({tieds/num_games}) | losses {losses} ({losses/num_games}) over {num_games} games") 





def main():
    game = quarto.Quarto()

    print("\nEvaluating HardCodedPlayer vs RandomPlayer:")
    evaluate(game, HardCodedPlayer(game), RandomPlayer(game))

    print("\nEvaluating MiniMaxPlayer vs RandomPlayer:")
    evaluate(game, MiniMaxPlayer(game), RandomPlayer(game))

    print("\nEvaluating MiniMaxPlayer vs HardCodedPlayer:")
    evaluate(game, MiniMaxPlayer(game), HardCodedPlayer(game))





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main()
