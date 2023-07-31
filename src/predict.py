from load_model import load_model
from ai.piece_classifier.model import predict_boards
import ai.color_classifier.model as cc
import ai.halfmove_counter.model as hc
import ai.fullmove_counter.model as fc
import paths
from fen.board import naively_check_castling_availability

def predict(img_arrs):
  board_strs = predict_boards(img_arrs, load_model(paths.PIECE_CLASSIFIER_MODEL))
  colors = cc.predictions(board_strs, load_model(paths.COLOR_CLASSIFIER_MODEL))
  castling_options = [naively_check_castling_availability(board) for board in board_strs]
  en_passants = list('-' * len(img_arrs)) # assume that en passant is not possible
  halfmoves = [str(i) for i in hc.predictions(board_strs, load_model(paths.HALFMOVE_COUNTER_MODEL))]
  fullmoves = [str(i) for i in fc.predictions(board_strs, load_model(paths.FULLMOVE_COUNTER_MODEL))]
  fens = zip(board_strs,colors,castling_options,en_passants,halfmoves,fullmoves)
  return [' '.join(fen) for fen in fens]
