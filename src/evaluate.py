import sys
from random import shuffle
from pathlib import Path
from argparse import ArgumentParser
from predict import predict
from paths import LICHESS_GAME_DATA_TEST_TXT
from viz.image import fen_str_to_image
from fen.fen import get_part,Part

parser = ArgumentParser()
parser.add_argument("-n", "--n", help="Number of tests")

def read_data():
  args = parser.parse_args()
  n_tests = None
  if args.n:
    if args.n.isnumeric():
      n_tests = int(args.n)
    else:
      print('-n must be a number!')
      sys.exit(-1)

  print(f'Reading lines from {Path(LICHESS_GAME_DATA_TEST_TXT).resolve()}')
  with open(LICHESS_GAME_DATA_TEST_TXT, 'r', encoding='utf-8') as f:
    fen_strs = f.readlines()
    if n_tests:
      shuffle(fen_strs)
      fen_strs = fen_strs[0:n_tests]

  return fen_strs

def compare_part(x,y,part):
  return get_part(x, part) == get_part(y, part)

def compute_diff(x,y,part):
  return abs(int(get_part(x, part)) - int(get_part(y, part)))

#pylint: disable=too-many-locals
def evaluate():
  fen_strs = read_data()

  count = len(fen_strs)

  # Correct counter
  boards          = 0
  colors          = 0
  castlings       = 0
  en_passants     = 0
  halfclocks      = 0
  halfclocks_diff = 0
  fullclocks      = 0
  fullclocks_diff = 0

  print(f'Evaluating {count} FEN-strings...')
  for i in range(0, count, 128):
    batch = fen_strs[i:i+128]
    xs = [fen_str_to_image(fen_str) for fen_str in batch]
    ys = predict(xs)
    for x,y in zip(batch,ys):
      boards          += compare_part(x,y,Part.BOARD)
      colors          += compare_part(x,y,Part.ACTIVE_COLOR)
      castlings       += compare_part(x,y,Part.CASTLING)
      en_passants     += compare_part(x,y,Part.EN_PASSANT)
      halfclocks      += compare_part(x,y,Part.HALFMOVE_CLOCK)
      halfclocks_diff += compute_diff(x,y,Part.HALFMOVE_CLOCK)
      fullclocks      += compare_part(x,y,Part.FULLMOVE_CLOCK)
      fullclocks_diff += compute_diff(x,y,Part.FULLMOVE_CLOCK)

  print('\n' + ('-' * 80))
  print(f"Evaluated {count} examples")
  print(f"'Board' accuracy: {boards/count:.3f}")
  print(f"'Active color' accuracy: {colors/count:.3f}")
  print(f"'Castling availability' accuracy: {castlings/count:.3f}")
  print(f"'En passant' accuracy: {en_passants/count:.3f}")
  print(f"'Halfmove clock' accuracy: {halfclocks/count:.3f}")
  print(f"Mean 'halfmove clock' difference: {halfclocks_diff/count:.3f}")
  print(f"'Fullmove clock' accuracy: {fullclocks/count:.3f}")
  print(f"Mean 'fullmove clock' difference: {fullclocks_diff/count:.3f}")

if __name__=='__main__':
  evaluate()
