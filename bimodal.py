# https://stackoverflow.com/a/35992526/5772735
from pylab import *
from scipy.optimize import curve_fit
import numpy as np

raw_data_path = 'data_sample/user_1_data.csv'

x1_frequency_path1 = 'data_sample/independent/x1_frequency_user_1_data.csv'
joint_frequency_path1 = 'data_sample/joint/joint_frequency_1.csv'
joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'
w_twod_gauss_params_txt_path1 = 'data_sample/gauss_params/2d_gauss_1.txt'
w_twod_gauss_params_txt_path2 = 'data_sample/gauss_params/2d_gauss_2.txt'

x1_list = []
x2_list = []
z_list = []


def process_data(frequency_r_path, gauss_w_path):
    file_data1 = np.loadtxt(frequency_r_path,
                            delimiter=',', skiprows=1)
    for col1, col2, col3 in file_data1:
        # sg.append([col1, col2])
        x1_list.append(col1)
        x2_list.append(col2)
        z_list.append(col3)
    return x1_list
    # fit_gaussian(gauss_w_path)


def process_1D_freq_data(frequency_r_path, gauss_w_path):
    file_data1 = np.loadtxt(frequency_r_path,
                            delimiter=',', skiprows=1)
    for col1, col2 in file_data1:
        # sg.append([col1, col2])
        x1_list.append(col1)
        z_list.append(col2)
    # fit_gaussian(gauss_w_path)
    return x1_list


def gauss(x, mu, sigma, A):
    return A*exp(-(x-mu)**2/2/sigma**2)


def fit():
    y = [11, 20, 19, 17, 10]
    y_bar = [12, 18, 19.5, 18, 9]
    summation = 0  # variable to store the summation of differences
    n = len(y)  # finding total number of items in list
    for i in range(0, n):  # looping through each element of the list
        # finding the difference between observed and predicted value
        difference = y[i] - y_bar[i]
        squared_difference = difference**2  # taking square of the differene
        # taking a sum of all the differences
        summation = summation + squared_difference
    MSE = summation/n  # dividing summation by total values to obtain average
    print("The Mean Square Error is: ", MSE)


def bimodal(x, mu1, sigma1, A1, mu2, sigma2, A2):
    return gauss(x, mu1, sigma1, A1)+gauss(x, mu2, sigma2, A2)


def main():
    data = process_1D_freq_data(
        x1_frequency_path1, w_twod_gauss_params_txt_path1)
    print("max(data)", max(data))
    print("min(data)", min(data))
    print("len(data)", len(data))
    # data = concatenate((normal(1, .2, 5000), normal(2, .2, 2500)))
    y, x, _ = hist(data, 100, alpha=.3, label='data')

    x = (x[1:]+x[:-1])/2  # for len(x)==len(y)
    expected = (1, .2, 250, 2, .2, 125)
    params, cov = curve_fit(bimodal, x, y, expected)
    sigma = sqrt(diag(cov))
    plot(x, bimodal(x, *params), color='red', lw=3, label='model')
    legend()
    print(params, '\n', sigma)
    fit()


if __name__ == "__main__":
    main()
