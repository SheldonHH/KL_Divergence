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

# raw_data_path = 'data_sample/user_1_data.csv'

json_user1_frequency_path = 'data_sample/independent/each_col_frequency_user1_data.json'
# joint_frequency_path1 = 'data_sample/joint/joint_frequency_1.csv'
# joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'
w_the_user_params_json = 'data_sample/joint/user1_params.json'
w_the_user_params_str = 'data_sample/joint/user1_params_'
# w_the_user_entropies_json = 'data_sample/joint/user1_entropies.json'
# w_the_user_entropies_sum_json = 'data_sample/joint/user1_entropies_sum.json'
w_twod_gauss_params_txt_path1 = 'data_sample/gauss_params/2d_gauss_1.txt'
w_twod_gauss_params_txt_path2 = 'data_sample/gauss_params/2d_gauss_2.txt'






def process_1D_freq_data(freq_dict):
    global global_entropy_list
    # global_entropy_list = []
    global this_col_entropy
    global x1_list
    global z_list
    x1_list = []
    z_list = []
    z_list = freq_dict.values()
    # print("x1_list", [float(i) for i in list(freq_dict.keys())])
    # print("z_list", list(freq_dict.values()))
    x1_list = [float(i) for i in list(freq_dict.keys())]
    z_list = list(freq_dict.values())
    return [float(i) for i in list(freq_dict.keys())]



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
def Average(lst):
    return mean(lst)
    
def variance(data):
     # Number of observations
     n = len(data)
     # Mean of the data
     mean = sum(data) / n
     # Square deviations
     deviations = [(x - mean) ** 2 for x in data]
     # Variance
     variance = sum(deviations) / n
     return variance

def stdev(data):
     var = variance(data)
     std_dev = math.sqrt(var)
     return std_dev

def main():
    counttttttt = 0
    user_params_list = []
    super_global_params = []
    super_global_entropies = []
    with open(json_user1_frequency_path, 'r') as f:
        person_dict = json.load(f)
    # ncol = len(person_dict)
    print("len(person_dict)",len(person_dict))
    for big_key, big_value in person_dict.items():
        print("person_dict", len(person_dict[big_key]))
        process_1D_freq_data(person_dict[big_key])
        print("max(data)", max(x1_list))
        print("min(data)", min(x1_list))
        print("len(data)", len(x1_list))
        peak = max(z_list)
        mean_x = sum(x1_list) / len(x1_list)
        print("mean0", mean_x)
        x_darray = np.asarray(x1_list, dtype=np.float32)
        z_darray = np.asarray(z_list, dtype=np.float32)
        mean_x = sum(x_darray * z_darray) / sum(z_darray)
        print("mean1", mean_x)
        meanx = Average(x1_list)
        sigma_x = np.sqrt(
            sum(z_darray * (x_darray - mean_x)**2) / sum(z_darray))
        print("sigma1", sigma_x)
        sigma_x = stdev(x1_list)
        print("sigma2", sigma_x)
        # print(sigma_x)
        # print(peak)
        # data = concatenate((normal(1, .2, 5000), normal(2, .2, 2500)))
        y, x, _ = hist(x1_list, len(x1_list)*2, alpha=.3, label='data')

        x = (x[1:]+x[:-1])/2  # for len(x)==len(y)
        x = x1_list
        y = z_list
        # bi_MSE = fit_bimodal(mean_x, sigma_x, peak, y, x)
        # mo_MSE = fit_one_modal(mean_x, sigma_x, peak, y, x)

        xSp = []
        ySp = []
        gauss_counter = 0
        #  while(gauss_counter < 4):
        # since the MSE could even increase for some data sets, we do from 1 to 10 Gauss curve_fit and choose the smallest MSE as result
        while(gauss_counter < 2):
            gauss_counter += 1
            xSp.append(gauss_counter)
            first_four_MSE = fit_multi_modal(
                mean_x, sigma_x, peak, y, x, gauss_counter)
            print(first_four_MSE)
            ySp.append(first_four_MSE)
        print("here", gauss_counter)
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
                # super_global_params.append(global_params)
                # super_global_entropies.append(global_entropy_list)
                # super_global_entropies.append(this_col_entropy)
                print("ySp", ySp)
                print("ySp.index(min(ySp))", ySp.index(min(ySp)))
                fit_multi_modal(mean_x, sigma_x, peak, y, x, ySp.index(min(ySp))+1)
                super_global_params = global_params
                counttttttt+=1
                print("≈",counttttttt)
                break
        single_d_params_dict = {}
        single_d_params_dict[big_key] = super_global_params
        write_dict_to_json(single_d_params_dict, w_the_user_params_str+big_key+".json")
        user_params_list.append(single_d_params_dict)
    write_dict_to_json({"user1": user_params_list}, w_the_user_params_json)
    fit_one_modal(mean_x, sigma_x, peak, y, x)
    y_for_sim = gauss(34.8, mean_x, sigma_x, peak)
    print("y_for_sim",y_for_sim)

def entropy1(labels, base=None):
    print("counts", entropy(labels))
    return entropy(labels)



def write_dict_to_json(dict, json_to_write):
    df_params = pd.DataFrame.from_dict(dict)
    result = df_params.to_json(orient="columns")
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))

if __name__ == "__main__":
    main()
