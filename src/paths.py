from pathlib import Path

STYLES                      = Path('../styles').resolve()
MODELS                      = Path('../models').resolve()
PIECE_TO_FEN_LABEl_MODEL    = Path(MODELS, 'piece_to_fen_label').resolve()
MOVE_COUNTER_MODEL          = Path(MODELS, 'move_counter').resolve()
INPUT_IMAGE                 = Path('../input.png').resolve()
OUTPUT_IMAGE                = Path('../output.png').resolve()
LICHESS_GAME_DATA_PGN       = Path('../lichess/lichess_game_data.pgn.zst')
LICHESS_GAME_DATA_TRAIN_TXT = Path('../lichess/lichess_game_data_train.txt')
LICHESS_GAME_DATA_TEST_TXT  = Path('../lichess/lichess_game_data_test.txt')
