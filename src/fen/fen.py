from enum import Enum
import numpy as np

# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
#                      0                      1  2   3 4 5
class Part(Enum):
  BOARD          = 0
  ACTIVE_COLOR   = 1
  CASTLING       = 2
  EN_PASSANT     = 3
  HALFMOVE_CLOCK = 4
  FULLMOVE_CLOCK = 5

def get_part(fen_str, part):
  return fen_str.split(' ')[part.value].strip()

def encode_color(color):
  return np.array([1,0]) if color == 'w' else np.array([0,1])

def decode_color(encoded_color):
  return 'w' if np.argmax(encoded_color) == 0 else 'b'
