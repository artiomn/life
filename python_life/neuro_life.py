#!/usr/bin/env python3

import h5py
import tensorflow as tf
import keras

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, , Input, Bidirectional, BatchNormalization
from keras.layers.recurrent import GRU, LSTM, SimpleRNN
from keras.utils import plot_model
from sys import argv

from gol_dataset import gen_xy_data

import tqdm

import numpy as np

iterations_count = 0
width = 0
height = 0

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

    #model.add(Convolution2D(8, 3, 3, input_shape=(1, width, height), activation='relu'))
    model.add(Dense(width * height, input_shape=(width, height), activation='linear'))
    model.add(Bidirectional(SimpleRNN(height * width, input_shape=(width, height), activation='relu',
                            return_sequences=True, recurrent_initializer='random_uniform', unroll=True),
                            merge_mode='sum'))
    #model.add(Bidirectional(GRU(height * width, input_shape=(width, height), activation='relu',
    #                        return_sequences=True, recurrent_initializer='uniform', unroll=True),
    #                        merge_mode='sum'))
#    model.add(SimpleRNN(height * width, input_shape=(width, height), activation='relu',
#                            return_sequences=True, recurrent_initializer='uniform', unroll=True))
    #model.add(Bidirectional(LSTM(width * height, input_shape=(width, height), activation='relu', return_sequences=True, unroll=True)))
    model.add(Dense(width * height, activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Bidirectional(SimpleRNN(height, activation='relu',
    #                        return_sequences=True, recurrent_initializer='uniform', unroll=False),
    #                        merge_mode='mul'))
    #model.add(SimpleRNN(height * width, input_shape=(width, height), activation='relu',
    #                        return_sequences=True, recurrent_initializer='uniform', unroll=True))
    model.add(BatchNormalization(momentum=0.995))
    model.add(Dense(height, activation='sigmoid'))

    model.summary()
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model


def test_predictions(model, width, height, iterations_count):
    x_test, y_test = gen_xy_data(width, height, iterations_count)

    predictions = model.predict(x_test)
    correct_predictions = 0
    print('Predictions testing started...')

    for i in tqdm.trange(len(x_test)):
        #print(x_train[i])
        test_arr = y_test[i] == predictions[i].round().astype(int)

        cc = 0
        for a in test_arr:
            for b in a:
                if b: cc += 1

        if (600 - cc) < 5: print('CC = {}'.format(cc))
        cc /= len(a) * len(test_arr)

        correct_predictions += cc
        if test_arr.all():
            print('Wow!')
            #correct_predictions += 1
        #print(predictions[i].round().astype(int))
        #print('x = %s, p = %s' % (x_train[i], y_new[i]))

    print('CC = {}'.format(correct_predictions / len(x_test)))


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
    #cb = keras.callbacks.TensorBoard(log_dir='keras_logs', write_graph=True)
    model.fit(x_train, y_train, epochs=1, verbose=1, validation_split=0.05) # callbacks=[cb])
    test_predictions(model, width, height, iterations_count)

