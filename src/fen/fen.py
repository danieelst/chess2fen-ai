# The classic starting position
STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
# Board with a piece per color per background color and lots of empty spaces
DATA_FEN = 'kkKKqqQQ/rrRRbbBB/nnNNppPP/8/8/8/8/8'

WHITE_LABEL = 'white'
BLACK_LABEL = 'black'

KING_LABEL   = 'k'
QUEEN_LABEL  = 'q'
ROOK_LABEL   = 'r'
BISHOP_LABEL = 'b'
KNIGHT_LABEL = 'n'
PAWN_LABEL   = 'p'
EMPTY_LABEL  = 'x'

# Black king, white king, ...
LABELS = 'kKqQrRbBnNpPx'

# The selection of pieces one side would have
PIECES = ''.join([KING_LABEL   * 1,
                  QUEEN_LABEL  * 1,
                  ROOK_LABEL   * 2,
                  BISHOP_LABEL * 2,
                  KNIGHT_LABEL * 2,
                  PAWN_LABEL   * 8,])

def to_white(piece):
  return piece.upper()

def is_white(piece):
  return piece.isupper()

def to_black(piece):
  return piece.lower()

def is_black(piece):
  return piece.islower()

def fen_str_to_1d_arr(fen_str):
  return [p for row in fen_str_to_2d_arr(fen_str) for p in row]

def fen_str_to_2d_arr(fen_str):
  expanded = ''.join(['x' * int(p) if p.isdigit() else p for p in fen_str])
  return list(expanded.split('/'))

def arr_to_fen_str(arr):
  return to_fen_str([(EMPTY_LABEL,None) if p==EMPTY_LABEL else
                     ((to_white(p),WHITE_LABEL) if is_white(p) else
                     (to_black(p),BLACK_LABEL)) for p in arr])

# Expects a string of pieces and empty squares denoted by their character
def count_empty(row):
  s = ''
  count = 0
  for square in row:
    if square == 'x':
      count += 1
    else:
      s = s + str(count) + square
      count = 0
  s += str(count)
  return s.replace('0','')

# Expects an Nx1 array of colorized pieces á la (PIECE,COLOR)
def row_to_fen_str(row):
  s = ''
  for square in row:
    (piece,color) = square
    if color == WHITE_LABEL:
      s += to_white(piece)
    elif color == BLACK_LABEL:
      s += to_black(piece)
    else:
      s += piece
  return count_empty(s)

# Expects a 64x1 array of colorized pieces á la (PIECE,COLOR)
def to_fen_str(board):
  rows = [board[i:i+8] for i in range(0,len(board),8)]
  return '/'.join([row_to_fen_str(row) for row in rows])

def fen_str_to_name(fen_str):
  return fen_str.replace('/','-')

def verify_fen_str(fen_str):
  arr = fen_str_to_2d_arr(fen_str)
  # Array is 8x8
  is_8x8 = len(arr) == 8 and all(len(row) == 8 for row in arr)
  # Array only contains valid labels
  has_valid_labels = all(p in LABELS for row in arr for p in row)
  return is_8x8 and has_valid_labels
