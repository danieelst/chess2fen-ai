import numpy as np
from PIL import Image
from chess import Board
import chess.svg as svg
from cairosvg import svg2png
from io import BytesIO

SIZE=256

def to_array(image):
  return np.array(image)

def from_array(img_arr):
  return Image.fromarray(img_arr)

def open_image(filepath):
  return to_array(_resize_image(Image.open(filepath)))

def _resize_image(image):
  return image.resize((SIZE,SIZE),Image.Resampling.LANCZOS)

def save_image(img_arr, filepath):
  from_array(img_arr).save(filepath)

def fen_str_to_image(fen_str):
  board = Board(fen_str) # Convert FEN string to board
  svg_board = svg.board(board,size=SIZE,coordinates=False) # Render board
  # Convert board into PNG-data
  mem = BytesIO()
  svg2png(svg_board,write_to=mem)
  # Read PNG-data as image
  img = Image.open(mem)
  # Convert to NumPy-array
  return to_array(img)
