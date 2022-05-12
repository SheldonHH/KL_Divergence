import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy import savetxt
import pickle

# You'll obviously need to reshape the output for plotting, e.g:
joint_frequency_path1 = 'data_sample/joint/joint_frequency_1.csv'
joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'


def twoD_Gaussian(point, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    x = point[0]
    y = point[1]
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude * \
        np.exp(- (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) + c*((y-yo)**2)))
    return g.ravel()


file_data1 = []
nnz = []
aau = []
iil = []


def process_data():
    file_data1 = np.loadtxt(joint_frequency_path1,
                            delimiter=',', skiprows=1)
    # sg = []

    for col1, col2, col3 in file_data1:
        # sg.append([col1, col2])
        nnz.append(col1)
        aau.append(col2)
        iil.append(col3)


def main():
    process_data()
    nz = np.asarray(nnz, dtype=np.float32)
    au = np.asarray(aau, dtype=np.float32)
    il = np.asarray(iil, dtype=np.float32)

    # x = np.linspace(0, 200, 201)
    # y = np.linspace(0, 200, 201)
    # x, y = np.meshgrid(x, y)
    arr = np.stack((nz, au), axis=1)
    print(type(arr))
    # weighted arithmetic mean (corrected - check the section below)
    mean_x = sum(nz * il) / sum(il)
    sigma_x = np.sqrt(sum(il * (nz - mean_x)**2) / sum(il))
    mean_y = sum(au * il) / sum(il)
    sigma_y = np.sqrt(sum(il * (au - mean_y)**2) / sum(il))
    print(mean_x)
    print(mean_y)
    second_guess = (max(il), mean_x, mean_y, sigma_x, sigma_y, 0, 10)

    data = twoD_Gaussian(arr, max(il), mean_x, mean_y, sigma_x, sigma_y, 0, 10)
    print(data.size)
    print(data)

    popt, pcov = curve_fit(twoD_Gaussian, data, il,
                           p0=second_guess, maxfev=500000)
    data_fitted = twoD_Gaussian(arr, *popt)
    print(popt)


if __name__ == "__main__":

    main()
