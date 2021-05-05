import os
import neat
import game.tk_gui as gui
import numpy as np

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

game.restart_game()
board = game.Board()

