from game import utils
from game.utils import Direction
# from game.ub4c106207f7d7ae4d7fb268df44519d4e1e
# from game.utils import Key
from game.utils import State
from game.utils import char_to_direction
from random import randint

EMPTY_TILE = 0
ID = 0

class GameCore:
    def __init__(self, game_size=4):
        self.game_size = game_size
        self.board = fresh_board(game_size)
        self.score = 0
        self.state = State.MENU
        self.move = 0

    def Score(self):
        return self.score

    def Move(self):
        return self.move

    def Board(self):
        return self.board

    def Game_size(self):
        return self.game_size

    def State(self):
        return self.state

    def restart_game(self, game_size=None):
        self.game_size = game_size if game_size is not None else self.game_size

        self.score = 0
        self.move = 0
        self.board = fresh_board(self.game_size)
        self.state = State.IDLE

        # Spawn two tiles randomly on the board
        self._spawn_tile(self.board)
        self._spawn_tile(self.board)

    def try_move(self, direction):
        if not has_move(self.board):
            self.state = State.LOSS
            return False

        moved = False
        rotations = 0
        back_rotations = 0
        if direction == Direction.UP:
            rotations = 2
            back_rotations = 2
            self.move += 1
        elif direction == Direction.DOWN:
            rotations = 0
            back_rotations = 0
            self.move += 1
        elif direction == Direction.LEFT:
            rotations = 3
            back_rotations = 1
            self.move += 1
        elif direction == Direction.RIGHT:
            rotations = 1
            back_rotations = 3
            self.move += 1
        else:
            return moved

        utils.rotate_clockwise(self.board, rotations)

        # Merge then shift through empty space
        merged = self._merge_down(self.board)
        shifted = self._shift_down(self.board)
        moved = merged or shifted

        utils.rotate_clockwise(self.board, back_rotations)

        if moved:
            self._spawn_tile(self.board)

        return moved

    # Can also be used to notify new tile to observers
    def _new_tile_appeared(self, new_tile_value):
        self.score = self.score + new_tile_value

    def _merge_down(self, board):
        merged = False
        for row in range(len(board) - 1, 0, -1):
            for col in range(0, len(board[row])):
                if board[row][col] != EMPTY_TILE:
                    if board[row][col] == board[row - 1][col]:
                        merged = True
                        new_value = board[row][col] + board[row - 1][col]
                        board[row][col] = new_value
                        board[row - 1][col] = EMPTY_TILE
                        self._new_tile_appeared(new_value)
        return merged

    # Shifts down tiles where there are empty spaces
    def _shift_down(self, board):
        shifted = False
        for row in range(len(board) - 1, -1, -1):
            for col in range(0, len(board[row])):
                temp_row = row
                while temp_row != len(board) - 1 and board[temp_row + 1][col] == EMPTY_TILE:
                    shifted = True
                    board[temp_row + 1][col] = board[temp_row][col]
                    board[temp_row][col] = EMPTY_TILE
                    temp_row = temp_row + 1

        return shifted

    # Randomly spawns a tile of value 2 or 4
    # P(x = 2) = 90%, P(x = 4) = 10%
    def _spawn_tile(self, board):
        spawned = False
        num_empty_tiles = count_value(board, EMPTY_TILE)
        if num_empty_tiles == 0:
            return spawned

        probability = randint(1, 100)
        tile_value = 2 if probability <= 90 else 4

        kth_selected_tile = randint(1, num_empty_tiles)
        current_empty_tile = 0
        for i, i_val in enumerate(board):
            for j, j_val in enumerate(i_val):
                if j_val == EMPTY_TILE:
                    current_empty_tile = current_empty_tile + 1
                    if current_empty_tile == kth_selected_tile:
                        board[i][j] = tile_value
                        spawned = True
                        break

            if spawned:
                self._new_tile_appeared(tile_value)
                break

        return spawned


def has_move(board):
    if count_value(board, EMPTY_TILE) > 0:
        return True

    _has_move = False
    for i in range(1, 5):
        _has_move = has_merge_down(board)
        if _has_move:
            # Rotate the board back
            utils.rotate_clockwise(board, 5 - i)
            return _has_move

        utils.rotate_clockwise(board)

    return _has_move


def has_merge_down(board):
    for row in range(len(board) - 1, 0, -1):
        for col in range(0, len(board[row])):
            if board[row][col] == board[row - 1][col]:
                return True
    return False


def fresh_board(size):
    return [[0 for i in range(0, size)] for j in range(0, size)]


# 2D array
def count_value(arr, value):
    count = 0
    for i in arr:
        for j in i:
            if j == value:
                count = count + 1

    return count



