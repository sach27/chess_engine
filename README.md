As of 1/08/23 it is a two player game, i.e. the AI engine is yet to be added to it, so it would not be possible to play against it.

However it has complete set of rules of chess programmed inside it so two players can play against each other like a normal chess board.

UPDATE

On 1/09/23 the engine has been complete, the chessmain file is for all the UI and for calling other two functions.

The engine file contains all the rules of chess encoded in them this includes castling on both sides, enpasent, pins, checkmate and stale mate.
This implies that anyone can use these two files to make a basic chess board along with all the rules coded in it and then just change 'move finder' file to experiment with the engine

The move finder files is based on standard chess hurestics and Nega-Max algorithm along with Alpha-Beta pruning, the hurestics of the engine are subjected to the experimentation and I will keep the repo open for any suggestions regarding better hurestics.
