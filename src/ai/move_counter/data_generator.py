from random import shuffle
import keras
import numpy as np
from paths import LICHESS_GAME_DATA_TRAIN_TXT
from fen.fen import get_part,Part,calculate_number_of_moves_made
from fen.board import str_to_1d_arr,encode_labels

OUTPUT_SHAPE=1

class DataGenerator(keras.utils.Sequence):
  def __init__(self, indexes, dimensions, batch_size=128):
    self.batch_size = batch_size
    self.dimensions = dimensions
    self.indexes = indexes
    self.on_epoch_end()

  def __len__(self):
    # Denotes the number of batches per epoch
    return int(np.floor(len(self.indexes) / self.batch_size))

  def __getitem__(self, batch_n):
    # Generate one batch of data
    batch_idxs = self.indexes[batch_n*self.batch_size:(batch_n+1)*self.batch_size]
    return self.__data_generation(batch_idxs)

  def on_epoch_end(self):
    shuffle(self.indexes)

  def __data_generation(self, batch_idxs):
    X = np.zeros((self.batch_size, *self.dimensions))
    y = np.zeros((self.batch_size, OUTPUT_SHAPE))

    with open(LICHESS_GAME_DATA_TRAIN_TXT, 'r', encoding='utf-8') as f:
      i = 0
      for idx, line in enumerate(f):
        if idx in batch_idxs:
          fen = line.rstrip()
          board = str_to_1d_arr(get_part(fen, Part.BOARD))
          moves = calculate_number_of_moves_made(get_part(fen, Part.ACTIVE_COLOR),
                                                 get_part(fen, Part.FULL_MOVE_CLOCK))

          X[i] = encode_labels(board)
          y[i] = moves
          i += 1

    return X, y

def file_size():
  with open(LICHESS_GAME_DATA_TRAIN_TXT, 'rbU') as f:
    return sum(1 for _ in f)
