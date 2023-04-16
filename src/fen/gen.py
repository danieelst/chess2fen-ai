from random import randint,shuffle
from fen.fen import PIECES,WHITE_LABEL,BLACK_LABEL,EMPTY_LABEL,to_fen_str

def randomize_pieces():
  n = randint(0,len(PIECES)) # 0 <= n <= l
  pieces = PIECES
  for i in range(0,n):
    l = list(pieces)
    shuffle(l)
    pieces = (''.join(l))[1:]
  return pieces

def random_fen_str():
  white_pieces = [(p,WHITE_LABEL) for p in randomize_pieces()]
  black_pieces = [(p,BLACK_LABEL) for p in randomize_pieces()]
  n = 8 * 8 - (len(white_pieces) + len(black_pieces)) # Number of empty squares
  empty_squares = [(EMPTY_LABEL,None) for i in range(0,n)]
  board = white_pieces + black_pieces + empty_squares
  shuffle(board)
  return to_fen_str(board)
