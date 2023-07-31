import numpy as np
from tensorflow.keras import Input,Model,layers        # type: ignore
from tensorflow.keras.callbacks import EarlyStopping   # type: ignore
from tensorflow.keras.losses import mean_squared_error # type: ignore
from paths import FULLMOVE_COUNTER_MODEL
from fen.fen import get_part,Part
from fen.board import str_to_1d_arr,encode_labels
from lichess.train_data_generator import get_generators

NAME='fullmove_counter_model'

#pylint: disable=duplicate-code

N_PIECES=64
N_LABELS=13

INPUT_SHAPE=(N_PIECES,N_LABELS)
OUTPUT_SHAPE=1

# Take 64 one-hot-encoded labels corresponding to the chess board (row by row)
# Output the number of fullmoves
def Fullmove_Counter_Model():
  inputs = Input(shape=INPUT_SHAPE)
  x = layers.Flatten()(inputs)
  x = layers.Dense(N_PIECES*N_LABELS, activation='relu')(x)
  output = layers.Dense(OUTPUT_SHAPE)(x)
  return Model(inputs=inputs, outputs=output, name=NAME)

def predict(board_str, model):
  return predictions([board_str], model)[0]

def predictions(board_strs, model):
  xs = np.array([encode_labels(str_to_1d_arr(board_str)) for board_str in board_strs])
  ys = model.predict(xs)
  return [round(y[0]) for y in ys]

def train_model(model=None, data_size=None, batch_size=128, epochs=1):
  def prep_data(fen):
    board = str_to_1d_arr(get_part(fen, Part.BOARD))
    fullmoves = get_part(fen, Part.FULLMOVE_CLOCK)
    return encode_labels(board), float(fullmoves)

  train, valid = get_generators(INPUT_SHAPE, OUTPUT_SHAPE, data_size, batch_size, prep_data)

  if model is None:
    model = Fullmove_Counter_Model()

  model.summary()

  model.compile(optimizer='adam',
                loss=mean_squared_error,
                metrics=['accuracy'])

  model.fit(train,
            epochs=epochs,
            validation_data=valid,
            callbacks=[EarlyStopping(monitor='loss', patience=3)])

  model.save(FULLMOVE_COUNTER_MODEL)
