import numpy as np
# from sklearn.mixture import GaussianMixture
# https://stackoverflow.com/a/35992526/5772735
from curses import raw
from ntpath import join
from re import S
from pylab import *
from scipy import linalg
from scipy.optimize import curve_fit
from scipy.stats import entropy
from sklearn import mixture
import numpy as np
import pandas as pd
import json
import random
import decimal
from scipy.interpolate import UnivariateSpline
import itertools
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl


# Creating a Function.
def simulated_height_normal_dist(x, mean, sd):
    prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
    return prob_density


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


def multi_bimodal(x, *params):
    print("*params", params)
    print("type(*params)", type(params))
    gausses = 0
    paramssss = params
    print("[0][0:3]", *params[0])
    index = 0
    gauss_index = int(len(*params)/3)
    for i in range(gauss_index):
        # print("i::",i)
        gausses += gauss(x, *params[0][0+index*3:3+index*3])
        index += 1

    return gausses


def read_from_csv(r_dense_trimmed_data_path1, before_extension_half, first_half):
    df = pd.read_csv(r_dense_trimmed_data_path1)
    return write_to_json(df, before_extension_half, first_half)


def write_to_json(df, before_extension_half, first_half):
    w_freq_path = first_half + \
        "independent/freq_"+before_extension_half+".json"
    w_percent_freq_path = first_half + \
        "independent/percent_freq_"+before_extension_half+".json"
    freq_json_file_to_write = open(w_freq_path, 'w')
    percent_freq_json_file_to_write = open(w_percent_freq_path, 'w')
    # json_file_to_write.write(json.dumps(df['x1'].value_counts().to_dict()))
    trimmed_dict = df.to_dict()
    freq_dict = {}

    count_dict = {}
    for key, value in trimmed_dict.items():
        freq_dict[key] = pd.DataFrame.from_dict(
            value, orient='index').value_counts().to_dict()
        print("len", len(freq_dict[key]))
        count_dict[key] = len(freq_dict[key])

    final_col_percentFreq_dict = {}
    final_col_freq_dict = {}
    for bigger_key, bigger_value in freq_dict.items():
        col_freq_dict = {}
        col_percentFreq_dict = {}
        for key, value in bigger_value.items():
            col_freq_dict[key[0]] = value
            col_percentFreq_dict[key[0]] = value / count_dict[bigger_key]
        final_col_freq_dict[bigger_key] = col_freq_dict
        final_col_percentFreq_dict[bigger_key] = col_percentFreq_dict
    freq_json_file_to_write.write(json.dumps(final_col_freq_dict))
    percent_freq_json_file_to_write.write(
        json.dumps(final_col_percentFreq_dict))
    return final_col_percentFreq_dict
    # with open(w_freq_path, 'r') as f:
    #     freq_dict = json.load(f)
    # with open(w_percent_freq_path, 'r') as f:
    #     freq_dict = json.load(f)


def plot_results(X, Y, means, covariances, index, title):
    splot = plt.subplot(5, 1, 1 + index)
    for i, (mean, covar, color) in enumerate(zip(means, covariances, color_iter)):
        v, w = linalg.eigh(covar)
        v = 2.0 * np.sqrt(2.0) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])
        # as the DP will not use every component it has access to
        # unless it needs it, we shouldn't plot the redundant
        # components.
        if not np.any(Y == i):
            continue
        plt.scatter(X[Y == i, 0], X[Y == i, 1], 0.8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan(u[1] / u[0])
        angle = 180.0 * angle / np.pi  # convert to degrees
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180.0 + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        splot.add_artist(ell)

    plt.xlim(-6.0, 4.0 * np.pi - 6.0)
    plt.ylim(-5.0, 5.0)
    plt.title(title)
    plt.xticks(())
    plt.yticks(())

#  The four initializations are
#  kmeans (default), random, random_from_data and k-means++.
#  eventual associated classification after GMM has finished


def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros


def main():
    args = sys.argv[1:]
    # print(args)
    # user_1_data
    raw_data_path1 = args[0]
    middle_index = args[0].rindex('/')
    last_index = len(args[0])-1
    first_half = args[0][0:middle_index+1]
    before_extension_half = args[0][middle_index+1: args[0].rindex('.')]
    r_dense_trimmed_data_path1 = first_half + \
        "trimmed/dense_trimmed_"+before_extension_half+".csv"
    final_col_percentFreq_dict = read_from_csv(
        r_dense_trimmed_data_path1, before_extension_half, first_half)

    # Parameters
    n_samples = 100

    # Generate random sample following a sine curve
    np.random.seed(0)
    X = np.zeros((n_samples, 2))
    # step = 4.0 * np.pi / n_samples

    # for i in range(X.shape[0]):
    #     x = i * step - 6.0
    # X[i, 0] = x + np.random.normal(0, 0.1)
    # X[i, 1] = 3.0 * (np.sin(x) + np.random.normal(0, 0.2))
    # print("final_col_percentFreq_dict",final_col_percentFreq_dict)
    i = 0
    for key, value in final_col_percentFreq_dict.items():
        # print("key", value)
        # print("value.keys()", list(value.keys()))
        n_samples = len(list(value.keys()))
        X = np.zeros((n_samples, 2))
        # for each dimension
        for i in range(len(list(value.keys()))):
            X[i, 0] = list(value.keys())[i]
            X[i, 1] = list(value.values())[i]
            i += 1
            # gmm1 = mixture.GaussianMixture(
            #     n_components=1, covariance_type="diag", max_iter=100).fit(X)
            # print("gmm1.covariances_", gmm1.covariances_)

        for index in range(10):
            gmm = mixture.GaussianMixture(
                n_components=index+1, covariance_type="diag", max_iter=100).fit(X)
            params = zerolistmaker((index+1)*3)
            print("index", index)
            print("gmm.means_", gmm.means_[index][0])
            params[index*3] = gmm.means_[index][0]
            params[index*3+1] = gmm.covariances_[index][0]
            params[index*3+2] = simulated_height_normal_dist(
                gmm.means_[index][0], gmm.means_[index][0], gmm.covariances_[index][0])
            ys_for_sim = []
            for g in range(n_samples):
                y_for_sim = multi_bimodal(
                    X[:, 0], *params)
                ys_for_sim.append(y_for_sim)
            # print("gmm.weights_", gmm.weights_)
            # print("gmm.covariances_", gmm.covariances_)
            # print("gmm.precisions_cholesky_", gmm.precisions_cholesky_)
            # print("sum(gmm.weights_)", sum(gmm.weights_))
            # print("gmm.means_", gmm.means_)
            #
            #
            # for sub_index in range(index+1):
            #     print("sub_index", sub_index)
            # params[sub_index*3] = gmm.means_[sub_index]
            #     params[sub_index*3+1] = gmm.covariances_array[sub_index][0]
            #     params[sub_index*3+2] = simulated_height_normal_dist(
            #         gmm.means_[sub_index], gmm.means_[sub_index], gmm.covariances_array[sub_index][0])
            #     # calculate the MSE for each Gauss number of test
            # ys_for_sim = []
            # for g in range(len(X[i, 0])):
            #     x_for_sim = float(decimal.Decimal(random.randrange(
            #         int(min(X[i, 0])*100), int(max(X[i, 0])*100)))/100)
            #     y_for_sim = multi_bimodal(
            #         x_for_sim, *params)
            #     ys_for_sim.append(y_for_sim)
        # print("gmm.weights_", gmm.weights_)
        # print("gmm.covariances_", gmm.covariances_)
        # print("gmm.precisions_cholesky_", gmm.precisions_cholesky_)
        # print("sum(gmm.weights_)", sum(gmm.weights_))
        # print("gmm.means_", gmm.means_)
    # plt.figure(figsize=(10, 10))
    # plt.subplots_adjust(
    #     bottom=0.04, top=0.95, hspace=0.2, wspace=0.05, left=0.03, right=0.97
    # )
    # Fit a Gaussian mixture with EM using ten components

    # plot_results(
    #     X, gmm.predict(X), gmm.means_, gmm.covariances_, 0, "Expectation-maximization"
    # )


if __name__ == "__main__":

    main()
