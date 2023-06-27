import sys
from pathlib import Path
from argparse import ArgumentParser
from fen.gen import random_fen_str
from fen.fen import verify_fen_str
from viz.image import fen_str_to_image,save_image,open_image
from ai.piece_to_fen.model import predict_board
from paths import PATH_TO_LATEST_MODEL,INPUT_IMAGE_PATH,OUTPUT_IMAGE_PATH
from load_model import load_model

parser = ArgumentParser()
parser.add_argument("-f", "--fen", help="Predict board generated from FEN-string")
parser.add_argument("-i", "--image", help="Predict FEN-string from provided board")

def main():
  args = parser.parse_args()
  fen_str = args.fen
  path_to_image = args.image
  img_arr = None

  if all([fen_str,path_to_image]):
    # Do not provide both args
    print('Provide either --fen or --image, not both!')
    sys.exit(-1)
  elif not path_to_image:
    # If only --fen was provided, use that
    # If no args provided, generate a random FEN-string
    if not fen_str:
      fen_str = random_fen_str()
      print(f'Randomizing FEN-string: {fen_str}')
    if not verify_fen_str(fen_str):
      print('FEN-string is not valid')
      sys.exit(-1)
    img_arr = fen_str_to_image(fen_str)
    save_image(img_arr, INPUT_IMAGE_PATH)
    print(f'\nConverting to board, see {Path(INPUT_IMAGE_PATH).resolve()}')
  elif path_to_image:
    # If --image was provided, use that
    print(f'\nReading image {Path(path_to_image).resolve()}')
    img_arr = open_image(path_to_image)
  else:
    # Quiet quitting
    sys.exit(-1)

  model = load_model(PATH_TO_LATEST_MODEL)
  new_fen_str = predict_board(img_arr, model)
  print(f'\nPredicted FEN-string: {new_fen_str}')
  save_image(fen_str_to_image(new_fen_str), OUTPUT_IMAGE_PATH)
  print(f'\nConverting to board, see {Path(OUTPUT_IMAGE_PATH).resolve()}')

if __name__=='__main__':
  main()
