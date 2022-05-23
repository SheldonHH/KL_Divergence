# https://stackoverflow.com/a/35992526/5772735
from curses import raw
from ntpath import join
from re import S
from pylab import *
from scipy.optimize import curve_fit
from scipy.stats import entropy
import numpy as np
import pandas as pd
import json
import random
import decimal
from scipy.interpolate import UnivariateSpline
import itertools
import csv

raw_data_path = 'data_sample/user_1_data.csv'

x1_frequency_path1 = 'data_sample/independent/x1_frequency_user_1_data.csv'
joint_frequency_path1 = 'data_sample/joint/joint_frequency_1.csv'
joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'
w_the_user_params_json = 'data_sample/joint/user_params.json'
w_the_user_entropies_json = 'data_sample/joint/user_entropies.json'
w_twod_gauss_params_txt_path1 = 'data_sample/gauss_params/2d_gauss_1.txt'
w_twod_gauss_params_txt_path2 = 'data_sample/gauss_params/2d_gauss_2.txt'


x1_list = []
z_list = []


def process_1D_freq_data(username, frequency_r_path, gauss_w_path, col_index):
    global global_entropy_list
    global_entropy_list = []
    file_data1 = np.loadtxt(frequency_r_path,
                            delimiter=',', skiprows=1)
    x1_list.clear()
    z_list.clear()
    for col1 in file_data1:
        x1_list.append(col1[col_index])
        z_list.append(col1[len(col1)-1])

    raw_x1_list = []
    raw_data_file_data = np.loadtxt(frequency_r_path,
                                    delimiter=',', skiprows=1)
    for col1 in raw_data_file_data:
        raw_x1_list.append(col1[col_index])
        x1_darray = np.asarray(raw_x1_list, dtype=np.float32)
    global_entropy_list.append(entropy1(x1_darray))
    return x1_list


def gauss(x, mu, sigma, A):
    return A*exp(-(x-mu)**2/2/sigma**2)


def fit(z_list, ys_for_sim):
    y = z_list
    y_bar = ys_for_sim
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
    return MSE


def gauss(x, mu, sigma, A):
    return A*exp(-(x-mu)**2/2/sigma**2)


def fit(z_list, ys_for_sim):
    y = z_list
    y_bar = ys_for_sim
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
    return MSE


def bimodal(x, mu1, sigma1, A1, mu2, sigma2, A2):
    return gauss(x, mu1, sigma1, A1)+gauss(x, mu2, sigma2, A2)


def fit_one_modal(mean_x, sigma_x, peak, y, x):
    expected = (mean_x, sigma_x, peak)
    params, cov = curve_fit(gauss, x, y, expected, maxfev=500000)
    sigma = sqrt(diag(cov))
    plot(x, gauss(x, *params), color='red', lw=3, label='model')
    legend()
    # print(params, '\n', sigma)
    print(params)
    ys_for_sim = []
    for g in range(len(x1_list)):
        x_for_sim = float(decimal.Decimal(random.randrange(
            int(min(x1_list)*100), int(max(x1_list)*100)))/100)
        y_for_sim = gauss(
            x_for_sim, *params)
        ys_for_sim.append(y_for_sim)
    return fit(z_list, ys_for_sim)


def fit_bimodal(mean_x, sigma_x, peak, y, x):
    expected = (mean_x, sigma_x, peak, mean_x, sigma_x, peak)
    params, cov = curve_fit(bimodal, x, y, expected, maxfev=500000)
    sigma = sqrt(diag(cov))
    plot(x, bimodal(x, *params), color='red', lw=3, label='model')
    legend()
    # print(params, '\n', sigma)
    # print(params)
    ys_for_sim = []
    for g in range(len(x1_list)):
        x_for_sim = float(decimal.Decimal(random.randrange(
            int(min(x1_list)*100), int(max(x1_list)*100)))/100)
        y_for_sim = bimodal(
            x_for_sim, *params)
        ys_for_sim.append(y_for_sim)
    return fit(z_list, ys_for_sim)


# def multi_bimodal(x, mu, sigma, A):
#     gausses = 0
#     # print("gauss_index", gauss_index)
#     for sg in range(gauss_index):
#         gausses += gauss(x, mu, sigma, A)
#     return gausses


def multi_bimodal(x, *params):
    gausses = 0
    # print("gauss_index", gauss_index)
    paramssss = params
    # print("paramssss", paramssss)
    index = 0
    for i in range(gauss_index):
        # print(i)
        # print("params[0+i*3:3+i*3]")
        # print(*params[0+index*3:3+index*3])
        gausses += gauss(x, *params[0+index*3:3+index*3])
        index += 1
    # if gauss_index == 5:

    return gausses


def fit_multi_modal(mean_x, sigma_x, peak, y, x, counter):
    global global_params
    global gauss_index
    gauss_index = counter
    expected = ()
    for i in range(counter):
        expected = expected + (mean_x, sigma_x, peak)
    params, cov = curve_fit(multi_bimodal, x, y, expected, maxfev=500000)
    global_params = params
    print("params: heee", params)
    print("params: lennnnnnnn", len(params))

    # MSE
    ys_for_sim = []
    for g in range(len(x1_list)):
        x_for_sim = float(decimal.Decimal(random.randrange(
            int(min(x1_list)*100), int(max(x1_list)*100)))/100)
        y_for_sim = multi_bimodal(
            x_for_sim, *params)
        ys_for_sim.append(y_for_sim)
    return fit(z_list, ys_for_sim)


gauss_index = 0

username = "user1"


def main():
    super_global_params = []
    super_global_entropies = []
    with open(raw_data_path, 'r') as csv:
        first_line = csv.readline()
        your_data = csv.readlines()

    ncol = first_line.count(',')
    for index in range(ncol):
        index_params = []
        print("index is", index)
        process_1D_freq_data(username,
                             raw_data_path, w_twod_gauss_params_txt_path1, index)
        print("ncol", ncol)
        print("max(data)", max(x1_list))
        print("min(data)", min(x1_list))
        print("len(data)", len(x1_list))
        peak = max(z_list)
        mean_x = sum(x1_list) / len(x1_list)
        print(mean_x)
        x_darray = np.asarray(x1_list, dtype=np.float32)
        z_darray = np.asarray(z_list, dtype=np.float32)
        mean_x = sum(x_darray * z_darray) / sum(z_darray)
        print(mean_x)
        sigma_x = np.sqrt(
            sum(z_darray * (x_darray - mean_x)**2) / sum(z_darray))
        # print(sigma_x)
        # print(peak)
        # data = concatenate((normal(1, .2, 5000), normal(2, .2, 2500)))
        y, x, _ = hist(x1_list, len(x1_list)*2, alpha=.3, label='data')

        x = (x[1:]+x[:-1])/2  # for len(x)==len(y)
        # bi_MSE = fit_bimodal(mean_x, sigma_x, peak, y, x)
        # mo_MSE = fit_one_modal(mean_x, sigma_x, peak, y, x)

        xSp = []
        ySp = []
        gauss_counter = 0
        while(gauss_counter < 4):
            gauss_counter += 1
            xSp.append(gauss_counter)
            first_four_MSE = fit_multi_modal(
                mean_x, sigma_x, peak, y, x, gauss_counter)
            print(first_four_MSE)
            ySp.append(first_four_MSE)

        print("here", gauss_counter)
        ysecond = 100000
        while(True):
            gauss_counter += 1
            after_four_MSE = fit_multi_modal(
                mean_x, sigma_x, peak, y, x, gauss_counter)
            print(after_four_MSE)
            print("after_four_MSE")
            ySp.append(after_four_MSE)
            xSp.append(gauss_counter)
            y_spl = UnivariateSpline(xSp, ySp, s=0, k=2)
            x_range = np.linspace(xSp[0], ySp[-1], len(xSp)-2)
            y_spl_2d = y_spl.derivative(n=2)
            if(abs(y_spl_2d(x_range)[-1]) < 0.1):
                print("gauss_index", gauss_index)
                print("global_params", global_params)
                super_global_params.append(global_params)
                super_global_entropies.append(global_entropy_list)
                break
    user_params_dict = {}
    user_params_dict["user1"] = super_global_params
    df_gauss = pd.DataFrame.from_dict(user_params_dict)
    result = df_gauss.to_json(orient="columns")
    parsed = json.loads(result)
    with open(w_the_user_params_json, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))

    user_entropies_dict = {}
    user_entropies_dict["user1"] = super_global_entropies
    df_entropy = pd.DataFrame.from_dict(user_entropies_dict)
    result = df_entropy.to_json(orient="columns")
    parsed = json.loads(result)
    with open(w_the_user_entropies_json, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))


def entropy1(labels, base=None):
    print("counts", entropy(labels))
    return entropy(labels)


if __name__ == "__main__":
    main()
