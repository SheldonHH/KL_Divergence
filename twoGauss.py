import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

def main():
    x0, y0 = 0.3, 0.7
    amp, a, b, c = 1, 2, 3, 4
    true_params = [amp, x0, y0, a, b, c]
    xy, zobs = generate_example_data(10, true_params)
    x, y = xy

    i = zobs.argmax()
    guess = [1, x[i], y[i], 1, 1, 1]
    pred_params, uncert_cov = opt.curve_fit(gauss2d, xy, zobs, p0=guess)

    zpred = gauss2d(xy, *pred_params)
    print ('True parameters: ', true_params)
    print ('Predicted params:', pred_params)
    print ('Residual, RMS(obs - pred):', np.sqrt(np.mean((zobs - zpred)**2)))

    plot(xy, zobs, pred_params)
    plt.show()

def gauss2d(xy, amp, x0, y0, a, b, c):
    x, y = xy
    inner = a * (x - x0)**2
    inner += 2 * b * (x - x0)**2 * (y - y0)**2
    inner += c * (y - y0)**2
    return amp * np.exp(-inner)

def generate_example_data(num, params):
    np.random.seed(1977) # For consistency
    xy = np.random.random((2, num))

    zobs = gauss2d(xy, *params)
    return xy, zobs

def plot(xy, zobs, pred_params):
    x, y = xy
    yi, xi = np.mgrid[:1:30j, -.2:1.2:30j]
    xyi = np.vstack([xi.ravel(), yi.ravel()])

    zpred = gauss2d(xyi, *pred_params)
    zpred.shape = xi.shape

    fig, ax = plt.subplots()
    ax.scatter(x, y, c=zobs, s=200, vmin=zpred.min(), vmax=zpred.max())
    im = ax.imshow(zpred, extent=[xi.min(), xi.max(), yi.max(), yi.min()],
                   aspect='auto')
    fig.colorbar(im)
    ax.invert_yaxis()
    return fig

# main()
