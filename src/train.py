from argparse import ArgumentParser
import ai.piece_to_fen_label.model as p2f
import ai.move_counter.model as mc
from load_model import load_model
from paths import MOVE_COUNTER_MODEL

parser = ArgumentParser()
parser.add_argument('-c', '--continue', action='store_true', help='Continue training')
parser.add_argument('-p2f', f'--{p2f.NAME}', action='store_true', help=f'Train {p2f.NAME}')
parser.add_argument('-mc', f'--{mc.NAME}', action='store_true', help=f'Train {mc.NAME}')


if __name__=='__main__':
  args = vars(parser.parse_args())
  if args[p2f.NAME]:
    print(f'Training {p2f.NAME}...')
    p2f.train_model()
  if args[mc.NAME]:
    print(f'Training {mc.NAME}...')
    MODEL = None
    if args['continue']:
      MODEL = load_model(MOVE_COUNTER_MODEL)
    mc.train_model(model=MODEL, data_size=200000, batch_size=128, epochs=1)
