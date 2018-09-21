#!/usr/bin/env python3

import h5py
import keras
import tqdm
import numpy as np
from sys import argv

from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
from keras.models import Sequential
from keras.layers import Dense, Dropout, Bidirectional, BatchNormalization
from keras.layers.recurrent import SimpleRNN
from keras.utils import plot_model

from gol_dataset import gen_xy_data


def read_xy_data(filename):
    print('Reading "{}"...'.format(filename))

    with h5py.File(filename, 'r') as f:
        x_train = np.array(f['x_train'])
        y_train = np.array(f['y_train'])

        iterations_count = len(x_train)
        width = len(x_train[0])
        height = len(x_train[0][0])

        assert iterations_count == len(y_train)
        assert width == len(y_train[0])
        assert height == len(y_train[0][0])

        return x_train, y_train


def generate_model(width, height):
    model = Sequential()

    model.add(Dense(width * height,
                    input_shape=(width, height),
                    activation='linear'))

    model.add(Bidirectional(SimpleRNN((height + 1) * (width + 1),
                                      input_shape=(width, height),
                                      activation='relu',
                                      return_sequences=True,
                                      recurrent_initializer='random_uniform',
                                      unroll=True),
                            merge_mode='sum'))
    model.add(SimpleRNN(height * width,
                        input_shape=(width, height),
                        activation='relu',
                        return_sequences=True,
                        recurrent_initializer='random_uniform',
                        unroll=True))
    model.add(Dense((width + 1) * (height + 1), activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(BatchNormalization(momentum=0.995))
    model.add(Dense(height, activation='sigmoid'))

    model.summary()
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model


def train_model(model, x_train, y_train, epochs=15, checkpoint_filename='checkpoint.hd5'):
    #cb = keras.callbacks.TensorBoard(log_dir='keras_logs', write_graph=True)
    try:
        print('Trying to load weights...')
        model.load_weights(checkpoint_filename)
        print('Weights were loaded...')
    except OSError as e:
        print(e)
    except ValueError as e:
        print('Incorrect checkpoint: {}'.format(e))

    checkpoint = ModelCheckpoint(checkpoint_filename,
                                 monitor='val_acc',
                                 verbose=1,
                                 save_weights_only=True,
                                 save_best_only=True,
                                 mode='max')
    rlr = ReduceLROnPlateau(monitor='val_loss',
                            verbose=1,
                            factor=0.2,
                            patience=2,
                            min_delta=0.001,
                            min_lr=0.001)
    es = EarlyStopping(monitor='val_acc',
                       verbose=1,
                       min_delta=0.001,
                       patience=4,
                       mode='max')
#                       restore_best_weights=True)
    model.fit(x_train,
              y_train,
              epochs=epochs,
              verbose=1,
              validation_split=0.05,
              callbacks=[es, rlr, checkpoint])
    print('Loading the best weights...')
    model.load_weights(checkpoint_filename)


def test_predictions(model, width, height, iterations_count):
    x_test, y_test = gen_xy_data(width, height, iterations_count)

    print('Prediction started...')
    predictions = model.predict(x_test)
    correct_predicted_steps = 0
    correct_predictions = 0
    print('Predictions testing started...')

    for i in tqdm.trange(len(x_test)):
        test_arr = y_test[i] == predictions[i].round().astype(int)

        cc = 0
        for a in test_arr:
            for b in a:
                if b:
                    cc += 1

        cc /= len(a) * len(test_arr)

        correct_predictions += cc
        if test_arr.all():
            correct_predicted_steps += 1

    print('Step\'s correct prediction rate = {}\nCorrect predicted steps = {}'.
          format(correct_predictions / len(x_test), correct_predicted_steps))


if __name__ == '__main__':
    print('Test task implementation')
    if len(argv) < 2:
        print('{} <data_filename>'.format(argv[0]))
        exit(1)

    x_train, y_train = read_xy_data(argv[1])

    iterations_count = len(x_train)
    width = len(x_train[0])
    height = len(x_train[0][0])

    model = generate_model(width, height)
    plot_model(model, to_file='model.png')

    train_model(model, x_train, y_train)

    test_predictions(model, width, height, iterations_count * 2)
