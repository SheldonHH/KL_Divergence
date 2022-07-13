from this import d
import pandas as pd
import numpy as np
import glob
import os
import csv
import re
import natsort
import pandas as pd
import sys
# import freq_to_gauss
import numpy as np
from tally import csv_to_jpeg
# from sklearn.mixture import GaussianMixture
# https://stackoverflow.com/a/35992526/5772735
from curses import raw
from ntpath import join
from re import S
import os
from pylab import *
from functools import reduce
from scipy import linalg
from scipy.optimize import curve_fit
from scipy.stats import entropy
from scipy.stats import norm
from sklearn import mixture
import pandas as pd
import json
from PIL import Image
import random
import decimal
from scipy.interpolate import UnivariateSpline
import itertools
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy import genfromtxt
import shutil
from expects import (
    be_true,
    equal,
    expect,
)

# Creating a Function.


def simulated_height_normal_dist(x, mean, sd):
    # prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
    # return prob_density
    # print(norm.cdf(x, mean, sd))
    return norm.cdf(x, mean, sd)


def calculate_MSE(z_list, ys_for_sim):
    y = z_list
    y_bar = ys_for_sim
    # print("z_list", z_list)
    # print("y_bar", y_bar)
    summation = 0  # variable to store the summation of differences
    n = len(y)  # finding total number of items in list
    for i in range(0, n):  # looping through each element of the list
        # finding the difference between observed and predicted value
        difference = y[i] - y_bar[i]
        squared_difference = difference**2  # taking square of the differene
        # taking a sum of all the differences
        summation = summation + squared_difference
    MSE = summation/n  # dividing summation by total values to obtain average
    # print("The Mean Square Error is: ", MSE)
    return MSE


def obtain_first_second(x, y, strtype):
    dy = np.diff(x, 1)
    dx = np.diff(y, 1)
    yfirst = dy/dx
    xfirst = 0.5*(x[:-1]+x[1:])
    dyfirst = np.diff(yfirst, 1)
    dxfirst = np.diff(xfirst, 1)

    if(strtype == "second"):
        ysecond = dyfirst/dxfirst
        # xsecond=0.5*(xfirst[:-1]+xfirst[1:])
        return ysecond
    else:
        return yfirst


def gauss(x, mu, sigma, A):
    return A*exp(-(x-mu)**2/2/sigma**2)


def multi_bimodal(x, weights_array, *params):
    gauss_index = int(len(params)/3)
    gausses = 0
    for i in range(gauss_index):
        gausses += weights_array[i]*gauss(x, *params[0+i*3:3+i*3])
    return gausses


def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros


def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)


def freq_to_gauss(true_datapath,  inputfile,  col_counter, raw_data_size, username):
    freq_dir = true_datapath+"/q/"+username+"/"
    uname = username
    # directory = os.path.join(freq_dir)
    os.chdir(freq_dir)
    num_with_params = {}  # (num_of_gauss, [params])
    num_with_weights = {}
    all_files_dimension_with_params = {}
    # for root,dirs,files in os.walk(directory):
    file = inputfile
    dimension_min_with_params = {}
    if file.endswith(".csv"):
        f = open(file, 'r')
        data_iter = csv.reader(f)
        data = [data for data in data_iter]
        final_list = []
        for row in data:
            row_list = []
            for item in row:
                row_list.append(float(item))
            final_list.append(row_list)
        X = np.array(final_list)
        # print("X[:,1]",X[:,1])
        # print("X[:,0]",X[:,0])
        # print("X",X)
        # break
        #  perform calculation
        f.close()
        MSE_list, ySp, xSp = [], [], []
        counter_initial = 5
        n_samples = len(data)
        for index in range(counter_initial):
            if n_samples < index+1:
                dimension_min_with_params.append(
                    {"gauss": num_with_params[min_index], "max": max(X[:, 0]), "min": min(X[:, 0])})
                break
            gmm = mixture.GaussianMixture(
                n_components=index+1, covariance_type="diag", max_iter=500000).fit(X)
            list_params = zerolistmaker((index+1)*3)
            simulated_y_sum = 0
            sort_mch = [[], [], [], []]  # means_cov_height
            for sub_index in range(index+1):
                sort_mch[0].append(gmm.weights_[sub_index])
                sort_mch[1].append(gmm.means_[sub_index][0])
                sort_mch[2].append(gmm.covariances_[sub_index][0])
                simulated_height = simulated_height_normal_dist(gmm.means_[sub_index][0], gmm.means_[
                                                                sub_index][0], math.sqrt(gmm.covariances_[sub_index][0]))*gmm.weights_[sub_index]
                sort_mch[3].append(simulated_height)
                simulated_y_sum += simulated_height
            # print(index,"simulated_y_sum",simulated_y_sum)
            sort_mch = np.array(list(map(list, zip(*sort_mch))))
            # print(sort_mch)
            # sg = sorted(sort_mch, key=lambda a_entry: sort_mch[0])
            sort_mch = sort_mch[sort_mch[:, 0].argsort(
                kind='mergesort')]  # sort by year
            # print("sgggg",sg)
            for sub_index in range(index+1):
                # print(sort_mch[sub_index])
                list_params[sub_index*3] = sort_mch[sub_index][1]
                list_params[sub_index*3+1] = sort_mch[sub_index][2]
                list_params[sub_index*3+2] = sort_mch[sub_index][3]
            params = tuple(list_params)
            num_with_params[index] = list_params
            num_with_weights[index] = [i[0] for i in sort_mch]
            # print("[i[0] for i in sort_mch]",[i[0] for i in sort_mch])
            # Calculate the MSE for each Gauss
            ys_for_sim = []  # different from assign the value
            for g in range(X[:, 0].size):
                x_for_sim = X[g][0]
                y_for_sim = multi_bimodal(
                    x_for_sim, gmm.weights_, *params)
                ys_for_sim.append(y_for_sim)
            MSE = calculate_MSE(X[:, 1].tolist(), ys_for_sim)
            ySp.append(MSE)
            xSp.append(index)
            MSE_list.append(MSE)
        incre_index = counter_initial

        while(True):
            min_index = 0
            if n_samples < incre_index+1:
                dimension_min_with_params.append(
                    {"gauss": num_with_params[min_index], "max": max(X[:, 0]), "min": min(X[:, 0])})
                break
            gmm = mixture.GaussianMixture(
                n_components=incre_index+1, covariance_type="diag", max_iter=100).fit(X)
            list_params = zerolistmaker((incre_index+1)*3)
            simulated_y_sum = 0
            for sub_index in range(incre_index+1):
                list_params[sub_index*3] = gmm.means_[sub_index][0]
                list_params[sub_index*3+1] = gmm.covariances_[sub_index][0]
                list_params[sub_index*3+2] = simulated_height_normal_dist(gmm.means_[sub_index][0], gmm.means_[
                                                                          sub_index][0], math.sqrt(gmm.covariances_[sub_index][0]))*gmm.weights_[sub_index]
                # print("simulated_height_normal_dist",list_params[sub_index*3+2]*gmm.weights_[sub_index])
                simulated_y_sum += list_params[sub_index *
                                               3+2]*gmm.weights_[sub_index]
            # print("TRUEsimulated_y_sum", simulated_y_sum)
            params = tuple(list_params)
            num_with_params[incre_index] = list_params
            # print(str(index+1),params,len(params))
            # Calculate the MSE for each Gauss
            ys_for_sim = []  # different from assign the value
            for g in range(X[:, 0].size):
                x_for_sim = X[g][0]
                y_for_sim = multi_bimodal(
                    x_for_sim, gmm.weights_, *params)
                ys_for_sim.append(y_for_sim)
            MSE = calculate_MSE(X[:, 1].tolist(), ys_for_sim)
            MSE_list.append(MSE)

            # print(MSE_list)
            # print("-----------------------------")
            ySp.append(MSE)
            # print("MSE", MSE)
            xSp.append(incre_index)

            y_firsts = obtain_first_second(
                np.array(ySp), np.array(xSp), "first")
            y_seconds = obtain_first_second(
                np.array(ySp), np.array(xSp), "second")
            if(abs(y_seconds[-1]) < 0.1 or y_firsts[-1] > 0 or incre_index == 100):

                print("incre_index", incre_index)
                # print("global_params", params)
                # print("ySp", ySp)
                # print("ySp.index(min(ySp))", ySp.index(min(ySp)))
                min_index = ySp.index(min(ySp))
                # print("xSp", xSp)
                # print("x_range",x_range)
                y_firsts = obtain_first_second(
                    np.array(ySp), np.array(xSp), "first")
                y_seconds = obtain_first_second(
                    np.array(ySp), np.array(xSp), "second")

                # print("y_seconds", y_seconds)
                # print("y_firsts", y_firsts)
                break
            incre_index += 1
      
        # print("num_with_weights", num_with_weights)
        minList = []
        maxList = []
        print(min_index)
        print(num_with_weights)
        if min_index in num_with_weights:
            dimension_min_with_params["weights"] = num_with_weights[min_index]
            dimension_min_with_params["gauss"] = num_with_params[min_index]
            minList, maxList = calculate_max_min(num_with_params[min_index])
        else:    
            dimension_min_with_params["weights"] = num_with_params[len(num_with_weights)-1]
            dimension_min_with_params["gauss"] = num_with_params[len(num_with_weights)-1]
            minList, maxList = calculate_max_min(num_with_params[len(num_with_weights)-1])
  
        # else:
        #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #     print(num_with_weights)
        #     return
        #     dimension_min_with_params["weights"] = num_with_weights[len(num_with_weights)-1]
        

        dimension_min_with_params["max"] = maxList
        dimension_min_with_params["min"] = minList
        dimension_min_with_params["raw_data_size"] = raw_data_size
        # print("type(X[:,0])", type(X[:, 0]))
        # plt.clf()
        # sorted_X = np.sort(X, axis=0)
        # plt.plot(sorted_X[:,0].tolist(), sorted_X[:,1].tolist(), 'b+:', label='data')
        # plt.plot(sorted_X[:,0].tolist(), multi_bimodal(
        #     sorted_X[:,0].tolist(), gmm.weights_, *tuple(num_with_params[min_index])), 'ro:', label='fit')
        # plt.legend()
        # plt.title("Dimension distribution for "+file)
        # plt.xlabel('Data')
        # plt.ylabel('Frequency')
        # fig = plt.gcf()
        # plt.show()
        # fig.savefig(file[0:findNth(file,"_",2)]+'.pdf')
        all_files_dimension_with_params[username +
                                        "_"+col_counter] = dimension_min_with_params
# path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    # os.remove(freq_dir+username+"_freq.csv")
    counterFolder = true_datapath+"users_individual_gauss/"+ col_counter+"/"
    if os.path.isdir(counterFolder) == False:
        os.mkdir(counterFolder)
        for f in glob.glob(counterFolder+"*.csv"):
            os.remove(f)
    with open(counterFolder + uname+"_"+col_counter+"_gauss.json", "w") as outfile:
        json.dump(all_files_dimension_with_params, outfile)
    # shutil.copyfile( uname+"_features_gauss_"+col_counter+".json", dir_str +
    #                 "users_individual_gauss/"+ uname+"_features_gauss_"+col_counter+".json")
    # os.remove(freq_dir+ uname+"_features_gauss".json")


# calculate max and min
def calculate_max_min(gaussList):
    minList = []
    maxList = []
    for sub_index in range(int(len(gaussList)/3)):
        mean = gaussList[sub_index*3] 
        sigma = gaussList[sub_index*3+1]
        ci = norm.interval(0.99, loc=mean, scale=sigma)
        print("ci")
        minList.append(ci[0])
        maxList.append(ci[1])
    return minList, maxList
    

def raw_data_size(username):
    numpy_array = np.loadtxt(
        "/home/xphuang/entropy/user_gauss_params/data/combine/"+username+"_combine.csv", delimiter=",")
    return len(numpy_array)


def f_to_g(Dir, username):
    rds = raw_data_size(username)
    this_user_dir = Dir+"users_individual_gauss/"+username+"/"
    if os.path.isdir(this_user_dir) == False:
        os.mkdir(this_user_dir)  # make dir for that user
    for feat_counter in range(4096):
        print(feat_counter)
        inputfile = Dir+"q/"+username+"/"+username+"_"+str(feat_counter)+"_q.csv"
        freq_to_gauss(Dir, inputfile, str(
            feat_counter), str(rds), username)

def main():
    t0 = time.time()
    username = "user_1"
    Dir = "/home/xphuang/entropy/user_gauss_params/data/"
     ####
    # i_and_freq(Dir,psedo_user_dir,username) # calculate Frequency
    # ####
    f_to_g(Dir, username)
    t1 = time.time()
    print(t1-t0)

    # raw_csv_path1 = psedo_user_dir
    # username = raw_csv_path1[raw_csv_path1.rindex(
    #     '/')+1: raw_csv_path1.rindex('.')]
    # # i_and_freq(Dir, psedo_user_dir, username)
    # f_to_g(Dir, psedo_user_dir, username)
    # inputfile = Dir + 'combine/combined_features.csv'
    # df = pd.read_csv(inputfile, header=None).T
    # for index, row in df.iterrows():
    #     countFreq(raw_csv_argv, row)


if __name__ == "__main__":
    main()
