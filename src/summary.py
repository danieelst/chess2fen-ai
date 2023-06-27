from load_model import load_model
from paths import PATH_TO_LATEST_MODEL

if __name__=='__main__':
  model = load_model(PATH_TO_LATEST_MODEL)
  model.summary()
