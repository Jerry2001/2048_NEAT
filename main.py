import os
import neat
import game.tk_gui as gui
import numpy as np

import visualize
from game import utils
from game.utils import Direction
from game.core_2048 import GameCore
from game.utils import State

game = GameCore(4)
GUI = gui.GameGUI(game)
NOT_MOVED_RESTART_THRESHOLD = 20

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
	net = neat.nn.FeedForwardNetwork.create(genome, config)
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
	#game.Score() + game.Max_tile()*5 - game.Move()

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

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 20)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    visualize.plot_stats(stats, ylog=False, view=True, filename="heapstats")
    visualize.plot_species(stats, view=True, filename= "heapspecies")
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    while(True):
    	winner_flag = not (input() == "False")
    	if(winner_flag == True):
    		winner_gif(winner_net)
    	else:
    		break

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)