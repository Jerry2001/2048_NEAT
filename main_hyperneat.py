import os
import neat
import game.tk_gui as gui
import numpy as np
import time

import visualize
from game import utils
from game.utils import Direction
from game.core_2048 import GameCore
from game.utils import State

from pureples.shared.visualize import draw_net
from pureples.shared.substrate import Substrate
from pureples.hyperneat.hyperneat import create_phenotype_network

try:
   import cPickle as pickle
except:
   import pickle

input_coordinates  = [(-1, 1), (0, 1), (1, 1), (2, 1), (-1, 0), (0, 0), (1, 0), (2, 0), (-1, -1), (0, -1), (1, -1), (2, -1), (-1, -2), (0, -2), (1, -2), (2, -2)]
output_coordinates = [(-1, 2), (0, 2), (1, 2), (2, 2)]
sub = Substrate(input_coordinates, output_coordinates)


game = GameCore(4)
GUI = gui.GameGUI(game)
NOT_MOVED_RESTART_THRESHOLD = 20

#for i in range(2, -3, -1):
#	for j in range(-1, 3):

def map_neuron_to_move(pos):
	if pos == 0:
		return Direction.UP
	elif pos == 1:
		return Direction.DOWN
	elif pos == 2:
		return Direction.LEFT
	elif pos == 3:
		return Direction.RIGHT

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        eval_genome(genome_id, genome, config)

def eval_genome(genome_id, genome, config):
	genome.fitness = 0.0
	cppn = neat.nn.FeedForwardNetwork.create(genome, config)
	net = create_phenotype_network(cppn, sub)

	#for i in range(0, 5):
	game.restart_game()
	GUI.set_game(game)
	game_over = False
	board = game.Board()
	consecutive_not_moved = 0
	successful_moves = 0

	while not game_over:
		in_neurons = (np.array(game.Board())).flatten()
		output = net.activate(in_neurons)
    	# Use the 'most activated' output neuron as the intended direction
        # Generate list of tuples which are (direction, output weight)
		output_moves = [(map_neuron_to_move(i), output[i]) for i in range(len(output))]
		output_moves = sorted(output_moves, key=lambda x: x[1])

        # Try move the board starting with the highest weighted output direction
		for (direction, weight) in output_moves:
			moved = game.try_move(direction)
			if moved:
				break

		if moved:
			GUI.repaint_board()
			successful_moves = successful_moves + 1
		else:
			consecutive_not_moved = consecutive_not_moved + 1

		if game.State() == State.WIN or game.State() == State.LOSS:
			game_over = True
		elif consecutive_not_moved == NOT_MOVED_RESTART_THRESHOLD:
			game_over = True
	genome.fitness = game.Score() 
	#genome.fitness /= 5.0

def winner_gif(winner_net):
	game.restart_game()
	GUI.set_game(game)
	game_over = False
	board = game.Board()
	consecutive_not_moved = 0
	successful_moves = 0

	while not game_over:
		in_neurons = (np.array(game.Board())).flatten()
		output = winner_net.activate(in_neurons)
    	# Use the 'most activated' output neuron as the intended direction
        # Generate list of tuples which are (direction, output weight)
		output_moves = [(map_neuron_to_move(i), output[i]) for i in range(len(output))]
		output_moves = sorted(output_moves, key=lambda x: x[1])

        # Try move the board starting with the highest weighted output direction
		for (direction, weight) in output_moves:
			moved = game.try_move(direction)
			if moved:
				break

		time.sleep(0.03)
		if moved:
			GUI.repaint_board()
			successful_moves = successful_moves + 1
		else:
			consecutive_not_moved = consecutive_not_moved + 1

		if game.State() == State.WIN or game.State() == State.LOSS:
			game_over = True
		elif consecutive_not_moved == NOT_MOVED_RESTART_THRESHOLD:
			game_over = True

# Create the population and run the XOR task by providing the above fitness function.
def run(config_file):
	config = neat.config.Config(neat.genome.DefaultGenome, neat.reproduction.DefaultReproduction,
                            neat.species.DefaultSpeciesSet, neat.stagnation.DefaultStagnation,
                            config_path)
	p = neat.population.Population(config)
	stats = neat.statistics.StatisticsReporter()
	p.add_reporter(stats)
	p.add_reporter(neat.reporting.StdOutReporter(True))

	winner = p.run(eval_genomes, 12)

    # Display the winning genome.
	print('\nBest genome:\n{!s}'.format(winner))
	visualize.plot_stats(stats, ylog=False, view=True, filename="hyperneatstats")
	visualize.plot_species(stats, view=True, filename= "hyperneatspecies")
	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
	while(True):
		winner_flag = not (input() == "False")
		if(winner_flag == True):
			winner_gif(winner_net)
		else:
			break

# If run as script.
if __name__ == '__main__':
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config_cppn')
	run(config_path)
	
    # Verify network output against training data.
    # print('\nOutput:')
    # cppn = neat.nn.FeedForwardNetwork.create(winner, config)
    # winner_net = create_phenotype_network(cppn, sub)
    # for inputs, expected in zip(xor_inputs, xor_outputs):
    #     new_input = inputs + (1.0,)
    #     winner_net.reset()
    #     for i in range(activations):
    #         output = winner_net.activate(new_input)
    #     print("  input {!r}, expected output {!r}, got {!r}".format(inputs, expected, output))

    # Save CPPN if wished reused and draw it to file along with the winner.
    # with open('hyperneat_xor_cppn.pkl', 'wb') as output:
    #     pickle.dump(cppn, output, pickle.HIGHEST_PROTOCOL)
    # draw_net(cppn, filename="hyperneat_xor_cppn")
    # draw_net(winner_net, filename="hyperneat_xor_winner")