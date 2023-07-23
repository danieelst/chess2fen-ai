from enum import Enum
import math

# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
#                      0                      1  2   3 4 5
class Part(Enum):
  BOARD           = 0
  ACTIVE_COLOR    = 1
  CASTLING        = 2
  EN_PASSANT      = 3
  HALF_MOVE_CLOCK = 4
  FULL_MOVE_CLOCK = 5

def get_part(fen_str, part):
  return fen_str.split(' ')[part.value]

def calculate_number_of_moves_made(active_color, full_move_clock):
  full_move_clock = int(full_move_clock) * 2
  return full_move_clock - 2 if active_color == 'w' else full_move_clock - 1

def calculate_full_move_clock(move_count):
  return math.floor(move_count / 2) + 1

def determine_active_color(move_count):
  return 'w' if move_count % 2 == 0 else 'b'
