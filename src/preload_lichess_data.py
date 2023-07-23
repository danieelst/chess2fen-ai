from lichess.game_sequence import filtered_fen_data_sequence
from paths import LICHESS_GAME_DATA_PGN,LICHESS_GAME_DATA_TRAIN_TXT,LICHESS_GAME_DATA_TEST_TXT

N_MOVES_TRAIN=10**6
N_MOVES_TEST=10**6

def write_to_file(path, fens):
  with open(path, 'w', encoding='utf-8') as f:
    print(f'Writing to {path.resolve()}...')
    f.write('\n'.join(str(i) for i in fens))

if __name__=='__main__':
  print(f'Reading {LICHESS_GAME_DATA_PGN.resolve()}...')
  print(f'Sequencing {N_MOVES_TRAIN + N_MOVES_TEST} moves, might take a while...')

  print('\033[?25l', end='') # remove cmd cursor

  train_fens = []
  test_fens = []
  for fen in filtered_fen_data_sequence():
    if len(train_fens) < N_MOVES_TRAIN:
      train_fens.append(fen)
      print(f'1/2: {len(train_fens)}/{N_MOVES_TRAIN}', end='\r')
    elif len(test_fens) < N_MOVES_TEST:
      print(f'2/2: {len(test_fens)}/{N_MOVES_TEST}', end='\r')
      test_fens.append(fen)
    else:
      break

  print('\033[?25h', end='') # restore cmd cursor

  write_to_file(LICHESS_GAME_DATA_TRAIN_TXT, train_fens)
  write_to_file(LICHESS_GAME_DATA_TEST_TXT, test_fens)
