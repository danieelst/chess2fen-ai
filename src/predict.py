from load_model import load_model
from ai.piece_to_fen_label.model import predict_boards
from ai.move_counter.model import predict_move_counts
from paths import PIECE_TO_FEN_LABEl_MODEL,MOVE_COUNTER_MODEL
from fen.fen import determine_active_color, calculate_full_move_clock
from fen.board import naively_check_castling_availability

P2F_MODEL = load_model(PIECE_TO_FEN_LABEl_MODEL)
MC_MODEL = load_model(MOVE_COUNTER_MODEL)

def predict(img_arrs):
  board_strs = predict_boards(img_arrs, P2F_MODEL)
  move_counts = predict_move_counts(board_strs, MC_MODEL)
  castling_options = [naively_check_castling_availability(board) for board in board_strs]
  colors = [determine_active_color(move_count) for move_count in move_counts]
  en_passants = list('-' * len(img_arrs)) # assume that en passant is not possible
  half_moves = list('?' * len(img_arrs))
  full_moves = [str(calculate_full_move_clock(move_count)) for move_count in move_counts]
  fens = zip(board_strs,colors,castling_options,en_passants,half_moves,full_moves)
  return [' '.join(fen) for fen in fens]
