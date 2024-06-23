# Quixo Project by Constantin Clipca (s290214)

For the project I submitted a Minmax solution with alpha beta pruning. 

## How to run the game

To run the game you need to launch the main.py file. By changing the players and players parameters in the main file you can see the performance of the agents.


## Changes to the given code

game.py:
1. ```move()```: added a public function that calls the private function __move() to be able to try moves from the minmax algorithm.
2. ```switch_player()```: added public function that switches the player.

main.py:
1. ```Node()```: class that keeps track of the parameters of a generic minmax algorithm.
2. ```MinmaxPlayer(Player)```: class where the minmax algorithm is implemented.
2. ```play_games(player1, player2, num_of_games)```: function that allows to evaluate 2 agents over a defined number of games.
