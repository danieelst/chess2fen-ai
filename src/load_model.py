# This file is a kind of a hack: it allows us to import TF and change
# the log level without PyLint too getting mad
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# pylint: disable=wrong-import-position
import tensorflow.keras.models as tf
# pylint: enable=wrong-import-position

# Simply wrap the function
def load_model(path):
  return tf.load_model(path)
