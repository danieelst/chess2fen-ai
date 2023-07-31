from argparse import ArgumentParser
import ai.piece_classifier.model as pc
import ai.color_classifier.model as cc
import ai.fullmove_counter.model as fc
import ai.halfmove_counter.model as hc
from load_model import load_model
from paths import COLOR_CLASSIFIER_MODEL, FULLMOVE_COUNTER_MODEL, HALFMOVE_COUNTER_MODEL

parser = ArgumentParser()
parser.add_argument('-c', '--continue', action='store_true', help='Continue training')
parser.add_argument('-pc', f'--{pc.NAME}', action='store_true', help=f'Train {pc.NAME}')
parser.add_argument('-cc', f'--{cc.NAME}', action='store_true', help=f'Train {cc.NAME}')
parser.add_argument('-fc', f'--{fc.NAME}', action='store_true', help=f'Train {fc.NAME}')
parser.add_argument('-hc', f'--{hc.NAME}', action='store_true', help=f'Train {hc.NAME}')

if __name__=='__main__':
  args = vars(parser.parse_args())
  # Train piece classifier
  if args[pc.NAME]:
    print(f'Training {pc.NAME}...')
    pc.train_model()

  # Train color classifier
  if args[cc.NAME]:
    print(f'Training {cc.NAME}...')
    MODEL = None
    if args['continue']:
      MODEL = load_model(COLOR_CLASSIFIER_MODEL)
    cc.train_model(model=MODEL, data_size=-1, batch_size=256, epochs=1)

  # Train fullmove counter model
  if args[fc.NAME]:
    print(f'Training {fc.NAME}...')
    MODEL = None
    if args['continue']:
      MODEL = load_model(FULLMOVE_COUNTER_MODEL)
    fc.train_model(model=MODEL, data_size=10000, batch_size=256, epochs=1)

  # Train halfmove counter model
  if args[hc.NAME]:
    print(f'Training {hc.NAME}...')
    MODEL = None
    if args['continue']:
      MODEL = load_model(HALFMOVE_COUNTER_MODEL)
    hc.train_model(model=MODEL, data_size=10000, batch_size=256, epochs=1)
