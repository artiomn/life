#!/usr/bin/env python3

import h5py
import numpy as np
import tqdm


class GameOfLife:
    @staticmethod
    def gen_random_state(width, height):
        state = (np.random.rand(width, height) * 2).astype(np.int32)
        return state

    @staticmethod
    def next_state(state):
        l_neib = np.roll(state, 1, 0)
        r_neib = np.roll(state, -1, 0)
        u_neib = np.roll(state, 1, 1)
        d_neib = np.roll(state, -1, 1)
        ul_neib = np.roll(l_neib, 1, 1)
        dl_neib = np.roll(l_neib, -1, 1)
        ur_neib = np.roll(r_neib, 1, 1)
        dr_neib = np.roll(r_neib, -1, 1)

        neibs = l_neib + r_neib + u_neib + d_neib + ul_neib + dl_neib + ur_neib + dr_neib
        next_state = np.copy(state)
        next_state[(neibs < 2) | (neibs > 3)] = 0
        next_state[neibs == 3] = 1

        return next_state


def gen_xy_data(width=20, height=30, n_samples=10000):
    print("Generate x_train")
    x_train = []
    for _ in tqdm.trange(n_samples):
        x_train.append(GameOfLife.gen_random_state(width, height))

    x_train = np.array(x_train)

    print("Generate y_train")
    y_train = np.zeros_like(x_train)
    for i, x in tqdm.tqdm(enumerate(x_train), total=len(x_train)):
        y_train[i] = GameOfLife.next_state(x)

    return x_train, y_train


if __name__ == "__main__":
    print("Generator started...")
    n_samples = 10000
    width = 20
    height = 30
    x_train = []
    y_train = []

    try:
        data_file = h5py.File("dataset_{width}x{height}x{n_samples}.h5".format(width=width, height=height, n_samples=n_samples), 'r')
        x_train = data_file["x_train"][:]
        y_train = data_file["y_train"][:]
        data_file.close()
    except OSError:
        x_train, y_train = gen_xy_data(width, height, n_samples)
        data_file = h5py.File("dataset_{width}x{height}x{n_samples}.h5".format(width=width, height=height, n_samples=n_samples), 'w')
        data_file.create_dataset("x_train", data=x_train)
        data_file.create_dataset("y_train", data=y_train)
        data_file.close()

    print("Dataset shape: {}".format(x_train.shape))

