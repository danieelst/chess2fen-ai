import tensorflow as tf
from tensorflow.keras import Input,Model,layers
from ai.generate_data import board_to_input,decode_output
from fen.fen import arr_to_fen_str

INPUT_SHAPE=(32,32,1)
OUTPUT_SHAPE=6*2+1 # Six chess piece types of two colors and the empty squares

# Takes an image á la 32x32 and predicts the piece in the image or if it is empty.
# Output is a one-hot encoded array
def Piece2FENLabelModel():
  inputs = Input(shape=INPUT_SHAPE)

  x = layers.Conv2D(32, (3,3), activation='relu')(inputs)
  x = layers.MaxPooling2D((2,2))(x)
  x = layers.Conv2D(64, (3,3), activation='relu')(x)
  x = layers.Flatten()(x)
  x = layers.Dense(64, activation='relu')(x)

  outputs = layers.Dense(OUTPUT_SHAPE)(x)

  return Model(inputs=inputs, outputs=outputs, name='piece2fen_label_model')

# Given a picture of the board, predict the FEN-string
def predict_board(img_arr, model):
  return predict_boards([img_arr], model)[0]

# Given a list of pictures boards, predict each FEN-string
def predict_boards(img_arrs, model):
  xs = tf.data.Dataset.from_tensors([square for board in
    [board_to_input(img_arr) for img_arr in img_arrs] for square in board])
  ys = model.predict(xs)
  # Divide the output into sections of size 64 (i.e. each square in a board)
  ys = [ys[i:i+64] for i in range(0,len(ys),64)]
  # Decode each section
  return [arr_to_fen_str([decode_output(p) for p in y]) for y in ys]
