from io import TextIOWrapper
from random import random
import zstandard as zstd
from chess.pgn import read_game
from paths import LICHESS_GAME_DATA_PGN

ELO_CUTOFF=1500
# Select 20% of the data
PERCENTAGE=0.2

def make_move(board,move):
  board.push(move)
  return board

def read_lichess_data(text_stream):
  game = read_game(text_stream)
  if game is None:
    return None
  w_elo = int(game.headers['WhiteElo'])
  b_elo = int(game.headers['BlackElo'])
  board = game.board()
  fens = [make_move(board,move).fen() for move in game.mainline_moves()]
  return w_elo, b_elo, fens

def _lichess_data_sequence():
  with open(LICHESS_GAME_DATA_PGN, 'rb') as fh:
    with zstd.ZstdDecompressor().stream_reader(fh) as reader:
      text_stream = TextIOWrapper(reader)
      while True:
        game = read_lichess_data(text_stream)
        if game is not None:
          yield game
        else:
          break

def fen_data_sequence():
  for _, _, fens in _lichess_data_sequence():
    for fen in fens:
      yield fen

def filtered_fen_data_sequence():
  for w_elo, b_elo, fens in _lichess_data_sequence():
    if w_elo >= ELO_CUTOFF and b_elo >= ELO_CUTOFF:
      for fen in fens:
        if random() < PERCENTAGE:
          yield fen
