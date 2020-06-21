# 2048 AI
An AI for the game 2048  

The AI with search depth 5 always gets the 16k tile, usually gets the 30k tile, and sometimes gets the 60k tile.  

The algorithm is simple minimax with a heuristic score. This algorithm isn't expectimax. Although the spawning is random, the randomness does not affect minimax from planning. I made it so the randomness is consistent across searches so the AI knows where tiles will spawn after a move. This obviously gives the AI a significant advantage over expectimax agents with less knowledge.

For the heuristic, I encourage the tiles to be arranged in a snaking pattern in decreasing order. This seems to be the optimal way to play. To be exact, I generated sequences of positions for each possible snaking hamiltonian path on the grid, and for each path, I used this formula to calculate a path score:  

$$
\sum_{v_i \in path} 0.5^{i-1}grid[v_i]
$$
Where $v_i$ is the $i$th position along the path and $grid[v_i]$ is the value of the tile at position $v_i$.

Then, I took the maximum path score out of all the snake paths and returned that as the score. This heuristic leads to the AI organizing the tiles in whichever snake path is optimal at the time.

# dependencies
* python >=3.6
* numpy

# running
run `python main.py 5` to run the AI with a search depth of 5