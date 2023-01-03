# Meron's Rush Hour Python Game

This is a Pygame version of the classic baord game "Rush Hour".

In the classic game the goal is to free the red car out of traffic jam.
The traffic is made of a set of 2 or 3 spaced viechles aligned verticaly or horizontaly across a 6X6 spaces board.
Cars may only be moved forward or backward to free place in the car's orientation in order to free the space for the red car to exit the board.

In this python based version of the game the app will generate random solvable game cards with different difficuklty levels according 
to the minimum number of moves needed in order to exit the red car.

The app will auto-solve generated game cards and store the solution path for an auto solution-player function.
Generated cards are saved in to a json file and can be loaded by specifing a difficulty level.

It is also possible to create your own game card car set and let the app auto-solve it and save it.

This app was built using Python and Pygame as for practicing Python Object Oriented Programming using a tre shotest-route search algorithm.

Have Fun!

Meron Gelbard

