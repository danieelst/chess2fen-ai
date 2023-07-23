import sys
from pathlib import Path
from argparse import ArgumentParser
from fen.board import verify_board_str
from fen.fen import get_part, Part
from viz.image import fen_str_to_image,save_image,open_image
from predict import predict
from paths import INPUT_IMAGE,OUTPUT_IMAGE

parser = ArgumentParser()
parser.add_argument('-f', '--fen',
                    help='Predict FEN-string from image generated with provided FEN-string')
parser.add_argument('-i', '--image',
                    help='Predict FEN-string from provided board')

def main():
  args = parser.parse_args()
  fen_str = args.fen
  path_to_image = args.image
  img_arr = None

  if all([fen_str,path_to_image]):
    # Do not provide both args
    print('Provide either --fen or --image, not both!')
    sys.exit(-1)
  elif path_to_image:
    # If --image was provided, use that
    print(f'\nReading image {Path(path_to_image).resolve()}')
    img_arr = open_image(path_to_image)
  elif fen_str:
    # If --fen was provided, use that
    if not verify_board_str(get_part(fen_str,Part.BOARD)):
      print('FEN-string is not valid')
      sys.exit(-1)
    img_arr = fen_str_to_image(fen_str)
    save_image(img_arr, INPUT_IMAGE)
    print(f'\nConverting to board, see {Path(INPUT_IMAGE).resolve()}')
  else:
    # Quiet quitting
    print('Provide either --fen or --image!')
    sys.exit(-1)

  new_fen_str = predict([img_arr])[0]
  print(f'\nPredicted FEN-string: {new_fen_str}')
  patched_fen_string = new_fen_str.replace('?','-',1).replace('?','0',1)
  save_image(fen_str_to_image(patched_fen_string), OUTPUT_IMAGE)
  print(f'\nConverting to board, see {Path(OUTPUT_IMAGE).resolve()}')

if __name__=='__main__':
  main()
