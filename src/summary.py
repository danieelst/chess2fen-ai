from load_model import load_model
import paths

if __name__=='__main__':
  load_model(paths.PIECE_CLASSIFIER_MODEL).summary()
  print()
  load_model(paths.COLOR_CLASSIFIER_MODEL).summary()
  print()
  load_model(paths.HALFMOVE_COUNTER_MODEL).summary()
  print()
  load_model(paths.FULLMOVE_COUNTER_MODEL).summary()
  print()
