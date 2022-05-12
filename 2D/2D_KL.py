# https://mail.python.org/pipermail/scipy-user/2011-May/029521.html

import numpy as np
from scipy.spatial import cKDTree as KDTree
import pandas as pd

joint_frequency_path1 = 'data_sample/joint/joint_frequency_1.csv'
joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'


def KLdivergence(x, y):
    # Check the dimensions are consistent
    x = np.atleast_2d(x)
    y = np.atleast_2d(y)

    n, d = x.shape
    m, dy = y.shape

    assert(d == dy)

    # Build a KD tree representation of the samples and find the nearest neighbour
    # of each point in x.
    xtree = KDTree(x)
    ytree = KDTree(y)
    # Get the first two nearest neighbours for x, since the closest one is the
    # sample itself.
    r = xtree.query(x, k=2, eps=.01, p=2)[0][:, 1]
    s = ytree.query(x, k=1, eps=.01, p=2)[0]
    print(r)
    print(s)

    # TODO fix
    # There is a mistake in the paper. In Eq. 14, the right side misses a negative sign
    # on the first term of the right hand side.
    return -np.log(r/s).sum() * d / n + np.log(m / (n - 1.))


data1 = []
data2 = []


def column(matrix, i, j):
    return [[row[i], row[j]] for row in matrix]


def read_data_from_csv():

    file_data1 = np.loadtxt(joint_frequency_path1,
                            delimiter=',', skiprows=1)
    file_data2 = np.loadtxt(joint_frequency_path2,
                            delimiter=',', skiprows=1)
    data1 = column(file_data1, 0, 1)
    data2 = column(file_data1, 0, 1)
    KLdivergence(data1, data2)


# p = data1
# q = data2


def main():
    read_data_from_csv()


if __name__ == "__main__":

    main()
