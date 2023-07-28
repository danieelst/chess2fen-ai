from random import shuffle
import numpy as np
from tensorflow.keras import Input,Model,layers
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import mean_absolute_error
from paths import MOVE_COUNTER_MODEL
from ai.move_counter.data_generator import DataGenerator,file_size,OUTPUT_SHAPE
from fen.board import str_to_1d_arr,encode_labels

NAME='move_counter_model'

N_PIECES=64
N_LABELS=13

INPUT_SHAPE=(N_PIECES,N_LABELS)

round_v = np.vectorize(round)

# Take 64 one-hot-encoded labels corresponding to the chess board (row by row)
# Output is a bit-array corresponding to the number of moves made
def Move_Counter_Model():
  inputs = Input(shape=INPUT_SHAPE)
  x = layers.Flatten()(inputs)
  x = layers.Dense(2048, activation='relu')(x)
  x = layers.Dense(1024, activation='relu')(x)
  x = layers.Dense(512,  activation='relu')(x)
  x = layers.Dense(256,  activation='relu')(x)
  x = layers.Dense(128,  activation='relu')(x)
  x = layers.Dense(64,   activation='relu')(x)
  x = layers.Dense(32,   activation='relu')(x)
  x = layers.Dense(16,   activation='relu')(x)
  x = layers.Dense(8,    activation='relu')(x)
  output = layers.Dense(OUTPUT_SHAPE)(x)
  return Model(inputs=inputs, outputs=output, name=NAME)

def predict_move_count(board_str, model):
  return predict_move_counts([board_str], model)[0]

def predict_move_counts(board_strs, model):
  xs = np.array([encode_labels(str_to_1d_arr(board_str)) for board_str in board_strs])
  ys = model.predict(xs)
  return [round(y[0]) for y in ys]

def train_model(model=None, data_size=-1, batch_size=128, epochs=3):
  idxs = list(range(0,file_size()))
  shuffle(idxs)
  if data_size > 0:
    idxs = idxs[:data_size]

  split = len(idxs) - batch_size

  train_generator = DataGenerator(indexes=idxs[0:split],
                                  dimensions=INPUT_SHAPE,
                                  batch_size=batch_size)
  valid_generator = DataGenerator(indexes=idxs[split:],
                                  dimensions=INPUT_SHAPE,
                                  batch_size=batch_size)

  if model is None:
    model = Move_Counter_Model()

  model.summary()

  model.compile(optimizer='adam',
                loss=mean_absolute_error,
                metrics=['accuracy'])

  model.fit(train_generator,
            epochs=epochs,
            validation_data=valid_generator,
            callbacks=[EarlyStopping(monitor='loss', patience=3)])

  model.save(MOVE_COUNTER_MODEL)
