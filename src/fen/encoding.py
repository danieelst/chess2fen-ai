import numpy as np
from fen.fen import LABELS

# Mapping from label to integer
LABEL_TO_INT = dict((l,i) for i,l in enumerate(LABELS))
INT_TO_LABEL = dict((i,l) for i,l in enumerate(LABELS))

# One-hot encoded label
def encode_label(label):
  zeros = np.zeros(len(LABELS))
  zeros[LABEL_TO_INT[label]] = 1
  return zeros

# Encode a list of labels
def encode_labels(labels):
  return np.asarray([encode_label(label) for label in labels])

# Decode one-hot encoded label
def decode_output(output):
  return INT_TO_LABEL[np.argmax(output)]
