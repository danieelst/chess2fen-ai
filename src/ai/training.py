from ai.generate_data import get_piece_label_pairs,normalize_images,encode_labels
from ai.model import Piece2FENLabelModel

from paths import PATH_TO_LATEST_MODEL

from pathlib import Path
from tensorflow.keras.losses import mean_squared_error

def train_model():
  pieces,labels = get_piece_label_pairs()
  normalized_pieces = normalize_images(pieces)
  encoded_labels = encode_labels(labels)

  n = int(len(normalized_pieces) * 0.9)

  # Split the data
  x_train = normalized_pieces[:n]
  y_train = encoded_labels[:n]
  x_test = normalized_pieces[n:]
  y_test = encoded_labels[n:]

  model = Piece2FENLabelModel()

  model.compile(optimizer='adam',
                loss=mean_squared_error,
                metrics=['accuracy'])

  model.fit(x_train,y_train,epochs=5)
  model.evaluate(x_test,y_test,verbose=2)

  model.save(PATH_TO_LATEST_MODEL)
