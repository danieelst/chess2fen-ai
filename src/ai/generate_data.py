import numpy as np
from pathlib import Path
from random import shuffle

from viz.image import open_image
from viz.processing import add_filter,image_to_grayscale,split_into_squares
import viz.filters as filters
from fen.fen import DATA_FEN,LABELS,fen_str_to_arr

from paths import PATH_TO_STYLES

def flatten(list_of_lists):
  return [item for sublist in list_of_lists for item in sublist]

# Given the images, create new images by applying the filter
def create_filtered_images(img_arrs, filt):
  return [add_filter(img_arr,filt) for img_arr in img_arrs]

def get_piece_label_pairs():
  # Get all images
  og_img_arrs = []
  for p in Path(PATH_TO_STYLES).glob('*.png'):
    print(f'Retrieving chess piece style "{p.stem}"...')
    fp = Path(PATH_TO_STYLES,p.name)
    og_img_arrs.append(open_image(fp))
  all_img_arrs = []
  all_img_arrs.extend(og_img_arrs)
  # Create more images by adding a filter for each piece style image
  all_img_arrs.extend(create_filtered_images(og_img_arrs,filters.RED))
  all_img_arrs.extend(create_filtered_images(og_img_arrs,filters.GREEN))
  all_img_arrs.extend(create_filtered_images(og_img_arrs,filters.BLUE))
  all_img_arrs.extend(create_filtered_images(og_img_arrs,filters.YELLOW))
  all_img_arrs.extend(create_filtered_images(og_img_arrs,filters.WHITE))
  all_img_arrs.extend(create_filtered_images(og_img_arrs,filters.GRAY))
  # Make all images grayscale
  grayscaled_img_arrs = [image_to_grayscale(img_arr) for img_arr in all_img_arrs]
  # Get an image for each square/piece
  grayscaled_pieces = flatten([split_into_squares(img_arr) for img_arr
                                                           in grayscaled_img_arrs])
  # Make a list of labels corresponding to the list of pieces above
  labels = fen_str_to_arr(DATA_FEN) * len(all_img_arrs)
  print(f'Generated {len(grayscaled_pieces)} (image-of-piece,label) pairs')
  # Shuffle the pieces and labels while still maintaining symmetry
  list_to_shuffle = list(zip(grayscaled_pieces,labels))
  shuffle(list_to_shuffle)
  pieces, labels = zip(*list_to_shuffle)
  return pieces,labels

def normalize_image(img_arr):
  return img_arr / 255.0

def normalize_images(img_arrs):
  return np.asarray([normalize_image(img_arr) for img_arr in img_arrs])

# Mapping from label to integer
label_to_int = dict((l,i) for i,l in enumerate(LABELS))
int_to_label = dict((i,l) for i,l in enumerate(LABELS))

# One-hot encoded label
def encode_label(label):
  zeros = np.zeros(len(LABELS))
  zeros[label_to_int[label]] = 1
  return zeros

# Encode a list of labels
def encode_labels(labels):
  return np.asarray([encode_label(label) for label in labels])

# Decode one-hot encoded label
def decode_output(output):
  return int_to_label[np.argmax(output)]

# Convert from an image array of a board, into input data
def board_to_input(img_arr):
  gray_img_arr = image_to_grayscale(img_arr)
  gray_img_arrs = split_into_squares(gray_img_arr)
  return normalize_images(gray_img_arrs)
