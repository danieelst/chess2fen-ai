# Models and Computations

Given an image, it will be scaled to a size of `256x256` pixels, grayscaled and naïvely divided into an `8x8` grid of `32x32` size images (i.e. one image per square in the board). The piece in each square will be determined by the `Piece_To_FEN_Label` model, and when each square has been determined, the board data can be computed.

From this, the castling availability will be naïvely determined (i.e. simply check if the kings and rooks have been moved).

From the board data, the amount of moves made will be determined with the `Move_Counter` model. With this we can compute the active color and the full-move clock.

En passant square is always assumed to be negative.

## `Piece_To_FEN_Label` model

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

## `Move_Counter` model

Expects an array of 64 one-hot encoded arrays of the 13 aforementioned classes. Will predict the number of moves made using regression.

The developed model is a fully-connected Neural Network, with the following layers:

```
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 input_1 (InputLayer)        [(None, 64, 13)]          0

 flatten (Flatten)           (None, 832)               0

 dense (Dense)               (None, 2048)              1705984

 dense_1 (Dense)             (None, 1024)              2098176

 dense_2 (Dense)             (None, 512)               524800

 dense_3 (Dense)             (None, 256)               131328

 dense_4 (Dense)             (None, 128)               32896

 dense_5 (Dense)             (None, 64)                8256

 dense_6 (Dense)             (None, 32)                2080

 dense_7 (Dense)             (None, 16)                528

 dense_8 (Dense)             (None, 8)                 136

 dense_9 (Dense)             (None, 1)                 9

=================================================================
Total params: 4504193 (17.18 MB)
Trainable params: 4504193 (17.18 MB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________
```

## Training the models

The models can be trained by running `python3 train.py`, using the options `-p2f` for the `Piece_To_FEN_Label` model and `-mc` for the `Move_Counter` model. Only one can be trained at once. Specify `-c` if you wish to train on an exsiting model.

The `Move_Counter` model will train on the data from `lichesss_game_data_train.txt`.

The `Piece_To_FEN_Label` model will be trained on images generated with different chess piece stylings and themes, see below:

### Generating chess pieces in different styles

I have captured a `256x256` PNG-image of each piece style available in Lichess (with some exceptions), with the default theme, using the FEN-string `kkKKqqQQ/rrRRbbBB/nnNNppPP/8/8/8/8/8`. These are available in `/styles`.

For each image, we apply a handful of filters to create new images (e.g. applying a green mask, thus creating a greener chess board image).

These are then grayscaled, normalized and divided into `8x8` grids. Each image in the grid is given a label of which piece it is in accordance to the FEN-string.
