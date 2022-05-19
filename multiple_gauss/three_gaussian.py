import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

data = np.genfromtxt('data.txt')


def gaussian(x, height, center, width, offset):
    return height*np.exp(-(x - center)**2/(2*width**2)) + offset


def three_gaussians(x, h1, c1, w1, h2, c2, w2, h3, c3, w3, offset):
    return (gaussian(x, h1, c1, w1, offset=0) +
            gaussian(x, h2, c2, w2, offset=0) +
            gaussian(x, h3, c3, w3, offset=0) + offset)


def two_gaussians(x, h1, c1, w1, h2, c2, w2, offset):
    return three_gaussians(x, h1, c1, w1, h2, c2, w2, 0, 0, 1, offset)


def errfunc3(p, x, y): return (three_gaussians(x, *p) - y)**2
def errfunc2(p, x, y): return (two_gaussians(x, *p) - y)**2


# I guess there are 3 peaks, 2 are clear, but between them there seems to be another one, based on the change in slope smoothness there
guess3 = [0.49, 0.55, 0.01, 0.6, 0.61, 0.01, 1, 0.64, 0.01, 0]
# I removed the peak I'm not too sure about
guess2 = [0.49, 0.55, 0.01, 1, 0.64, 0.01, 0]
optim3, success = optimize.leastsq(
    errfunc3, guess3[:], args=(data[:, 0], data[:, 1]))
optim2, success = optimize.leastsq(
    errfunc2, guess2[:], args=(data[:, 0], data[:, 1]))
optim3

plt.plot(data[:, 0], data[:, 1], lw=5, c='g', label='measurement')
plt.plot(data[:, 0], three_gaussians(data[:, 0], *optim3),
         lw=3, c='b', label='fit of 3 Gaussians')
plt.plot(data[:, 0], two_gaussians(data[:, 0], *optim2),
         lw=1, c='r', ls='--', label='fit of 2 Gaussians')
plt.legend(loc='best')
plt.savefig('result.png')
