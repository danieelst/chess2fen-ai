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

def evaluate():
  fen_strs = read_data()

  count = len(fen_strs)

  # Correct counter
  boards      = 0
  colors      = 0
  castlings   = 0
  full_clocks = 0

  print(f'Evaluating {count} FEN-strings...')
  for i in range(0, count, 128):
    batch = fen_strs[i:i+128]
    xs = [fen_str_to_image(fen_str) for fen_str in batch]
    ys = predict(xs)
    for x,y in zip(batch,ys):
      boards += get_part(x, Part.BOARD)        == get_part(y, Part.BOARD)
      colors += get_part(x, Part.ACTIVE_COLOR) == get_part(y, Part.ACTIVE_COLOR)
      castlings += get_part(x, Part.CASTLING)  == get_part(y, Part.CASTLING)
      clock_x = int(get_part(x, Part.FULL_MOVE_CLOCK))
      clock_y = int(get_part(y, Part.FULL_MOVE_CLOCK))
      clock_x1 = clock_x
      # We want the same accuracy even if the predicted number is larger
      if clock_x < clock_y:
        clock_x1 *= 2
      full_clocks += (clock_x1 - clock_y) / clock_x

  print('\n' + ('-' * 80))
  print(f"Evaluated {count} examples")
  print(f"'Board' accuracy: {boards/count}")
  print(f"'Active color' accuracy: {colors/count}")
  print(f"'Castling availability' accuracy: {castlings/count}")
  print(f"'Full move clock' accuracy: {full_clocks/count}")

if __name__=='__main__':
  evaluate()
