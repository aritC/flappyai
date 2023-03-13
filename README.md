# flappyai

AI trying to Play Flappy Bird clone

![Training  GIF](./train.gif)

## Description of AI

I created an AI which learns to play flappy bird. It uses [NEAT algorithm](https://neat-python.readthedocs.io/en/latest/neat_overview.html) to learn the game and what its supposed to do. I use 3 nodes in for input and 1 for output. The inputs to the algorithm are:

- Bird's Y position as the bird's x position is always constant
- Distance from the incoming top pipe
- and Distance from the incoming bottom pipe

Then I use sigmoid as the activation function since sigmoid will squash all the value to 0 or 1 which tell the AI whether it should make the bird jump or not.

After each generation I choose to only keep the best bird and have set a fitness threshold of 100. If the bird manages to pass a pipe I reward it with 5 points and if it either colides with the pipe or the ground I deduct 1 point from the fitness. Apart from that every loop I add 0.05 points all the alive bird's fitness for helping AI to focus on staying alive as long as possible as well.

## Description of Game

The flappy bird game was created using [Pygame](https://www.pygame.org/docs/). There are 4 .py file which I'll explain below:

- base.py: Classfile for the base or the ground. It loads 2 copies of the base img and loops the base images to make the impression of a never ending base image.

- bird.py: Classfile for bird. It loads the bird's images and animates them. It has bunch of utility related to the bird like move, draw ,etc.

- pipe.py: Classfile for the pipes. It loads a single pipe's img and flips it with a constant GAP but random heights to create a new obstacle course every time. Apart from that this also contains the method to check for collision of the pipe with the bird.

- flappy.py: Main file where all the code comes together. Here I render the game objects in the pygame window and initialize and train the Neural Network.

## Assets and Config

All assets used in this code can be found [here](https://github.com/samuelcust/flappy-bird-assets/tree/master/sprites)

Got the basic config file from [here](https://github.com/CodeReclaimers/neat-python/blob/master/examples/xor/config-feedforward)
