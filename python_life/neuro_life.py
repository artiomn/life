#!/usr/bin/env python3

import h5py
import keras
import tqdm
import numpy as np
from sys import argv

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

    model.add(Bidirectional(SimpleRNN(height * width,
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
                        recurrent_initializer='uniform',
                        unroll=True))
    model.add(Dense(width * height, activation='relu'))
    #model.add(Dropout(0.1))
    model.add(BatchNormalization(momentum=0.995))
    model.add(Dense(height, activation='sigmoid'))

    model.summary()
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model


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

    print('Step correct prediction rate = {}\nCorrect predicted steps = {}'.
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

    #cb = keras.callbacks.TensorBoard(log_dir='keras_logs', write_graph=True)
    model.fit(x_train,
              y_train,
              epochs=15,
              verbose=1,
              validation_split=0.05) # callbacks=[cb])
    test_predictions(model, width, height, iterations_count)
