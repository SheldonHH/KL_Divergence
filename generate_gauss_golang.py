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
import matplotlib.pyplot as plt

# raw_data_path = 'data_sample/user_1_data.csv'

# json_user1_frequency_path = 'data_sample/independent/each_col_frequency_user1_data.json'
# joint_frequency_path1 = 'data_sample/joint/joint_frequency_1.csv'
# joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'
# w_the_user_params_json = 'data_sample/joint/user1_params.json'
# w_the_user_entropies_json = 'data_sample/joint/user1_entropies.json'
# w_the_user_entropies_sum_json = 'data_sample/joint/user1_entropies_sum.json'
# w_twod_gauss_params_txt_path1 = 'data_sample/gauss_params/2d_gauss_1.txt'
# w_twod_gauss_params_txt_path2 = 'data_sample/gauss_params/2d_gauss_2.txt'


def create_fig(x, y, title, *params):
    plt.clf()
    plt.plot(x, y, 'b+:', label='data')
    plt.plot(x, gauss(x, *params), 'ro:', label='fit')
    plt.legend()
    plt.title("Dimension distribution for "+title)
    plt.xlabel('Frequency')
    plt.ylabel('data')
    fig = plt.gcf()
    plt.show()
    str_params = [(str(tup)) for tup in params]
    print("str_params", str_params)
    plt.text(5, 8, ''.join(str_params), fontsize=10)
    fig.savefig("./figs"+title+'.pdf')


def process_1D_freq_data(freq_dict):
    sorted_freq_dict = {k: v for k, v in sorted(list(freq_dict.items()))}
    global global_entropy_list
    # global_entropy_list = []
    global this_col_entropy
    global x1_list
    global z_list
    x1_list = []
    z_list = []
    z_list = sorted_freq_dict.values()
    # print("x1_list", [float(i) for i in list(sorted_freq_dict.keys())])
    # print("z_list", list(sorted_freq_dict.values()))
    x1_list = [float(i) for i in list(sorted_freq_dict.keys())]
    z_list = list(sorted_freq_dict.values())
    return [float(i) for i in list(sorted_freq_dict.keys())]


def calculate_MSE(z_list, ys_for_sim):
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
    global special_one_gauss
    expected = (mean_x, sigma_x, peak)
    params, cov = curve_fit(gauss, x, y, expected, maxfev=500000)
    sigma = sqrt(diag(cov))
    plot(x, gauss(x, *params), color='red', lw=3, label='model')
    legend()
    # print(params, '\n', sigma)
    print(params)
    special_one_gauss = params
    ys_for_sim = []
    for g in range(len(x1_list)):
        x_for_sim = float(decimal.Decimal(random.randrange(
            int(min(x1_list)*100), int(max(x1_list)*100)))/100)
        x_for_sim = x1_list[g]
        y_for_sim = gauss(
            x_for_sim, *params)
        ys_for_sim.append(y_for_sim)
    return calculate_MSE(z_list, ys_for_sim)


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
        x_for_sim = x1_list[g]
        y_for_sim = bimodal(
            x_for_sim, *params)
        ys_for_sim.append(y_for_sim)
    return calculate_MSE(z_list, ys_for_sim)


# def multi_bimodal(x, mu, sigma, A):
#     gausses = 0
#     # print("gauss_index", gauss_index)
#     for sg in range(gauss_index):
#         gausses += gauss(x, mu, sigma, A)
#     return gausses


def multi_bimodal(x, *params):
    gausses = 0
    index = 0
    for i in range(gauss_index):
        gausses += gauss(x, *params[0+index*3:3+index*3])
        index += 1
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
    # print("params: heee", params)
    print("params: lennnnnnnn", len(params))

    # MSE
    ys_for_sim = []
    for g in range(len(x1_list)):
        x_for_sim = float(decimal.Decimal(random.randrange(
            int(min(x1_list)*100), int(max(x1_list)*100)))/100)
        y_for_sim = multi_bimodal(
            x_for_sim, *params)
        ys_for_sim.append(y_for_sim)
    return calculate_MSE(z_list, ys_for_sim)


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
    args = sys.argv[1:]
    raw_data_path1 = args[0]
    middle_index = args[0].rindex('/')
    last_index = len(args[0])-1
    first_half = args[0][0:middle_index+1]
    before_extension_half = args[0][middle_index+1: args[0].rindex('.')]
    each_col_freq_path = first_half + \
        "independent/each_col_freq_"+before_extension_half+".json"
    w_the_user_params_json = first_half+'joint/'+before_extension_half+'_params.json'
    print(each_col_freq_path, "each_col_freq_path")
    print(w_the_user_params_json, "w_the_user_params_json")

    counttttttt = 0
    user_params_list = []
    super_global_params = []
    super_global_entropies = []
    with open(each_col_freq_path, 'r') as f:
        person_dict = json.load(f)
    for big_key, big_value in person_dict.items():
        print("person_dict", len(person_dict[big_key]))
        process_1D_freq_data(person_dict[big_key])
        print("max(data)", max(x1_list))
        print("min(data)", min(x1_list))
        print("len(data)", len(x1_list))
        peak = max(z_list)
        print("peak", peak)
        mean_x = sum(x1_list) / len(x1_list)
        print("mean0", mean_x)
        x_darray = np.asarray(x1_list, dtype=np.float32)
        z_darray = np.asarray(z_list, dtype=np.float32)
        mean_x = sum(x_darray * z_darray) / sum(z_darray)
        print("mean1", mean_x)
        meanx = Average(x1_list)
        print("mean2", mean_x)
        sigma_x = np.sqrt(
            sum(z_darray * (x_darray - mean_x)**2) / sum(z_darray))
        print("sigma1", sigma_x)
        sigma_x = stdev(x1_list)
        print("sigma2", sigma_x)
        # print(sigma_x)
        # print(peak)
        # data = concatenate((normal(1, .2, 5000), normal(2, .2, 2500)))
        # y, x, _ = hist(x1_list, len(x1_list)*2, alpha=.3, label='data')

        # x = (x[1:]+x[:-1])/2  # for len(x)==len(y)
        x = x1_list
        y = z_list
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
        while(True):
            gauss_counter += 1
            after_four_MSE = fit_multi_modal(
                mean_x, sigma_x, peak, y, x, gauss_counter)
            print(after_four_MSE)
            print("-----------------------------")
            ySp.append(after_four_MSE)
            xSp.append(gauss_counter)
            y_spl = UnivariateSpline(xSp, ySp, s=0, k=2)
            x_range = np.linspace(xSp[0], ySp[-1], len(xSp)-2)
            y_spl_1d = y_spl.derivative(n=1)
            y_spl_2d = y_spl.derivative(n=2)
            print("ySp", ySp)
            print("y_spl_1d(x_range)", y_spl_1d(x_range))
            print("y_spl_2d(x_range)", y_spl_2d(x_range))
            if(abs(y_spl_2d(x_range)[-1]) < 0.1 or y_spl_1d(x_range)[-1] > 0):
                print("gauss_index", gauss_index)
                print("global_params", global_params)
                # super_global_params.append(global_params)
                # super_global_entropies.append(global_entropy_list)
                # super_global_entropies.append(this_col_entropy)
                print("ySp", ySp)
                print("ySp.index(min(ySp))", ySp.index(min(ySp)))
                fit_multi_modal(mean_x, sigma_x, peak, y,
                                x, ySp.index(min(ySp))+1)
                super_global_params = global_params
                plt.clf()
                plt.plot(x, y, 'b+:', label='data')
                plt.plot(x, multi_bimodal(
                    x, *global_params), 'ro:', label='fit')
                plt.legend()
                plt.title("Dimension distribution for "+big_key)
                plt.xlabel('Frequency')
                plt.ylabel('data')
                fig = plt.gcf()
                plt.show()
                fig.savefig("./figs"+big_key+'fig1.pdf')
                counttttttt += 1
                print("≈", counttttttt)
                break
        single_d_params_dict = {}
        single_d_params_dict[big_key] = super_global_params
        single_d_params_dict["max"] = max(x1_list)
        single_d_params_dict["min"] = min(x1_list)
        user_params_list.append(single_d_params_dict)
        fit_one_modal(mean_x, sigma_x, peak, y, x)
        create_fig(x, y, big_key+"special one dimensional gauss",
                   *special_one_gauss)

    write_dict_to_json({"user1": user_params_list}, w_the_user_params_json)

    # y_for_sim = gauss(34.8, mean_x, sigma_x, peak)
    # print("y_for_sim",y_for_sim)


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
