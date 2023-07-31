# Models and Computations

Given an image, it will be scaled to a size of `256x256` pixels, grayscaled and naïvely divided into an `8x8` grid of `32x32` size images (i.e. one image per square in the board). The piece in each square will be determined by the `Piece_Classifier` model, and when each square has been determined, the board data can be computed.

From the board data, the castling availability will be naïvely determined (i.e. simply check if the kings and rooks have been moved), the active color will be determined with the `Color_Classifier` model, and the number of moves made will be determined with the `Halfmove_Counter` model and the `Fullmove_Counter` model.

En passant square is always assumed to be negative (which is correct in nearly all cases).

## `Piece_Classifier` model

Expects a `32x32`, normalized and grayscaled image of square from a chess board, and will predict the label corresponding to the content of the square (i.e. either a piece or empty). The output is a one-hot encoded array corresponding to the 13 classes (six types of pieces of two possible colors, and the empty square).

The developed model is a Convolutional Neural Network, with the following layers:

```
_________________________________________________________________
 Layer (type)                 Output Shape             Param #
=================================================================
 input_1 (InputLayer)         [(None, 32, 32, 1)]      0

 conv2d (Conv2D)              (None, 30, 30, 32)       320

 max_pooling2d (MaxPooling2D) (None, 15, 15, 32)       0

 conv2d_1 (Conv2D)            (None, 13, 13, 64)       18496

 flatten (Flatten)            (None, 10816)            0

 dense (Dense)                (None, 64)               692288

 dense_1 (Dense)              (None, 13)               845

=================================================================
Total params: 711,949
Trainable params: 711,949
Non-trainable params: 0
_________________________________________________________________
```

## `Color_Classifier` model

Expects an array of 64 one-hot encoded arrays of the 13 aforementioned classes. Will predict one of the two classes: white or black.

The developed model is a fully-connected Neural Network, with the following layers:

```
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 input_1 (InputLayer)        [(None, 64, 13)]          0

 flatten (Flatten)           (None, 832)               0

 dense (Dense)               (None, 128)               106624

 dense_1 (Dense)             (None, 128)               16512

 dense_2 (Dense)             (None, 128)               16512

 dense_3 (Dense)             (None, 2)                 258

=================================================================
Total params: 139906 (546.51 KB)
Trainable params: 139906 (546.51 KB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________
```

## `Halfmove_Counter` model

Expects an array of 64 one-hot encoded arrays of the 13 aforementioned classes. Will predict the number of halfmoves made.

The developed model is a fully-connected Neural Network, with the following layers:

```
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 input_2 (InputLayer)        [(None, 64, 13)]          0

 flatten_1 (Flatten)         (None, 832)               0

 dense_2 (Dense)             (None, 832)               693056

 dense_3 (Dense)             (None, 1)                 833

=================================================================
Total params: 693889 (2.65 MB)
Trainable params: 693889 (2.65 MB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________
```

## `Fullmove_Counter` model

Expects an array of 64 one-hot encoded arrays of the 13 aforementioned classes. Will predict the number of fullmoves made.

The developed model is a fully-connected Neural Network, with the following layers:

```
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 input_1 (InputLayer)        [(None, 64, 13)]          0

 flatten (Flatten)           (None, 832)               0

 dense (Dense)               (None, 832)               693056

 dense_1 (Dense)             (None, 1)                 833

=================================================================
Total params: 693889 (2.65 MB)
Trainable params: 693889 (2.65 MB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________
```

## Training the models

The models can be trained by running `python3 train.py`, using the options `-pc` for the `Piece_Classifier` model, `-cc` for the `Color_Classifier` model, `-hc` for the `Halfmove_Counter` model and `-fc` for the `Fullmove_Counter` model. Specify `-c` if you wish to train on an exsiting model.

The `Color_Classifier` model, the `Halfmove_Counter` model and the `Fullmove_Counter` model will train on the data from `lichess_game_data_train.txt`.

The `Piece_Classifier` model will be trained on images generated with different chess piece stylings and themes, see below:

### Generating chess pieces in different styles

I have captured a `256x256` PNG-image of each piece style available in Lichess (with some exceptions), with the default theme, using the FEN-string `kkKKqqQQ/rrRRbbBB/nnNNppPP/8/8/8/8/8`. These are available in `/styles`.

For each image, we apply a handful of filters to create new images (e.g. applying a green mask, thus creating a greener chess board image).

These are then grayscaled, normalized and divided into `8x8` grids. Each image in the grid is given a label of which piece it is in accordance to the FEN-string.
