from load_model import load_model
from paths import PIECE_TO_FEN_LABEl_MODEL,MOVE_COUNTER_MODEL

if __name__=='__main__':
  load_model(PIECE_TO_FEN_LABEl_MODEL).summary()
  print()
  load_model(MOVE_COUNTER_MODEL).summary()
