import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow.keras.models import load_model

from paths import PATH_TO_LATEST_MODEL

if __name__=='__main__':
  model = load_model(PATH_TO_LATEST_MODEL)
  model.summary()
