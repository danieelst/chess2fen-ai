from random import shuffle
import keras
import numpy as np
from paths import LICHESS_GAME_DATA_TRAIN_TXT

class TrainDataGenerator(keras.utils.Sequence):
  #pylint: disable=too-many-arguments
  def __init__(self, indexes, input_shape, output_shape, fen_to_x_and_y, batch_size):
    self.indexes        = indexes
    self.input_shape    = input_shape
    self.output_shape   = output_shape
    self.fen_to_x_and_y = fen_to_x_and_y
    self.batch_size     = batch_size
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
    X = np.zeros((self.batch_size, *self.input_shape))
    # Try and see if the variable is iterable
    try:
      y = np.zeros((self.batch_size, *self.output_shape))
    except TypeError:
      y = np.zeros((self.batch_size, self.output_shape))

    with open(LICHESS_GAME_DATA_TRAIN_TXT, 'r', encoding='utf-8') as f:
      i = 0
      for idx, line in enumerate(f):
        if idx in batch_idxs:
          fen = line.rstrip()
          xi, yi = self.fen_to_x_and_y(fen)
          X[i] = xi
          y[i] = yi
          i += 1

    return X, y

def file_size():
  with open(LICHESS_GAME_DATA_TRAIN_TXT, 'rbU') as f:
    return sum(1 for _ in f)

def get_generators(input_shape, output_shape, data_size, batch_size, fen_to_x_and_y):
  idxs = list(range(0,file_size()))
  shuffle(idxs)
  if data_size is not None:
    idxs = idxs[:data_size]
  split = len(idxs) - batch_size
  train_generator = TrainDataGenerator(indexes=idxs[0:split],
                                       input_shape=input_shape,
                                       output_shape=output_shape,
                                       fen_to_x_and_y=fen_to_x_and_y,
                                       batch_size=batch_size)
  valid_generator = TrainDataGenerator(indexes=idxs[split:],
                                       input_shape=input_shape,
                                       output_shape=output_shape,
                                       fen_to_x_and_y=fen_to_x_and_y,
                                       batch_size=batch_size)
  return train_generator, valid_generator
