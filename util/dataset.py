import numpy as np
import random


def gen_normal_data(mu, sigma, size, seed=None):
    np.random.seed(seed)

    data = np.random.normal(loc=mu, scale=sigma, size=size)
    data = np.rint(data)

    return data


def save_data(data, file=None, gzip=False):
    if gzip == True:
        file = file + ".gz"

    np.savetxt(file, data[None, :], fmt="%d", delimiter=',\n')


data = gen_normal_data(0, 100, 1000000)
save_data(data, file="./vec.out")
save_data(data, file="./vec.out", gzip=True)
