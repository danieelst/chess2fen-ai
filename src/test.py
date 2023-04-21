'''A simple little program to automatically test N randomized FEN-strings on
the model.
'''
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from fen.gen import random_fen_str
from fen.fen import verify_fen_str
from viz.image import fen_str_to_image
from argparse import ArgumentParser
from tensorflow.keras.models import load_model
from ai.model import predict_boards
from paths import PATH_TO_LATEST_MODEL

parser = ArgumentParser()
parser.add_argument("-n", "--n", help="Number of tests")

if __name__=='__main__':
  args = parser.parse_args()
  N_TESTS = 100 if not args.n or not args.n.isnumeric() else int(args.n)
  print(f'Generating {N_TESTS} cases...')
  fen_strs = []
  for i in range(0,N_TESTS):
    fen_strs.append(random_fen_str())
  if all([verify_fen_str(fen_str) for fen_str in fen_strs]):
    print('All generated FEN-strings are valid')
  else:
    print('Not all generated FEN-strings are valid')
    exit(-1)
  img_arrs = [fen_str_to_image(fen_str) for fen_str in fen_strs]
  model = load_model(PATH_TO_LATEST_MODEL)
  print('Predicting...')
  p_fen_strs = predict_boards(img_arrs, model)
  results = [x==y for (x,y) in zip(fen_strs,p_fen_strs)]
  passed = [True for b in results if b]
  failed = [False for b in results if not b]
  print(f'{len(passed)} \u2713, {len(failed)} X')
