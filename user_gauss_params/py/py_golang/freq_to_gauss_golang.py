import numpy as np
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
    dy=np.diff(x,1)
    dx=np.diff(y,1)
    yfirst=dy/dx
    xfirst=0.5*(x[:-1]+x[1:])
    dyfirst=np.diff(yfirst,1)
    dxfirst=np.diff(xfirst,1)
    
    if(strtype == "second"):
        ysecond=dyfirst/dxfirst
        xsecond=0.5*(xfirst[:-1]+xfirst[1:])
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
        # print("len", len(freq_dict[key]))
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




def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros


def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)

def main():
    args = sys.argv[1:]
    raw_csv_path1 = args[0]
    dir_str = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    freq_dir = dir_str+"/features/freq/"
    gauss_filetype = "dynamic"
    directory = os.path.join(freq_dir)
    os.chdir(freq_dir)   
    num_with_params = {} # (num_of_gauss, [params])
    num_with_weights = {}
    all_files_dimension_with_params = {}
    for root,dirs,files in os.walk(directory):
        for file in files:
            dimension_min_with_params = {}
            if file.endswith(".csv"):
                f=open(file, 'r')
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
                MSE_list, ySp, xSp = [],[],[]
                y_firsts, y_seconds = [],[]
                counter_initial = 10
                n_samples = len(data)
                final_weights = 0
                for index in range(counter_initial):
                    if n_samples < index+1:
                        dimension_min_with_params.append({key+"_gauss": num_with_params[min_index],"max":max(X[:,0]),"min":min(X[:,0])})
                        break
                    gmm = mixture.GaussianMixture(n_components=index+1, covariance_type="diag", max_iter=500000).fit(X)
                    list_params = []
                    list_params = zerolistmaker((index+1)*3)
                    params = tuple(list_params)
                    # print("index", index)
                    # print("gmm.means_", gmm.means_[index][0])
                    simulated_y_sum = 0
                    sort_mch = [[],[],[],[]] # means_cov_height
                    for sub_index in range(index+1):
                        sort_mch[0].append(gmm.weights_[sub_index])
                        sort_mch[1].append(gmm.means_[sub_index][0])
                        sort_mch[2].append(gmm.covariances_[sub_index][0])
                        simulated_height = simulated_height_normal_dist(gmm.means_[sub_index][0], gmm.means_[sub_index][0], math.sqrt(gmm.covariances_[sub_index][0]))*gmm.weights_[sub_index]
                        sort_mch[3].append(simulated_height)
                        simulated_y_sum += simulated_height
                    # print(index,"simulated_y_sum",simulated_y_sum)
                    sort_mch = np.array(list(map(list, zip(*sort_mch))))
                    print(sort_mch)
                    # sg = sorted(sort_mch, key=lambda a_entry: sort_mch[0]) 
                    sort_mch = sort_mch[sort_mch[:, 0].argsort(kind='mergesort')]  # sort by year
                    # print("sgggg",sg)
                    for sub_index in range(index+1):
                        list_params[sub_index*3] = sort_mch[sub_index][1]
                        list_params[sub_index*3+1] = sort_mch[sub_index][2]
                        list_params[sub_index*3+2] = sort_mch[sub_index][3]
                    params = tuple(list_params)
                    num_with_params[index] = list_params
                    num_with_weights[index] = [i[0] for i in sort_mch]
                    # print("[i[0] for i in sort_mch]",[i[0] for i in sort_mch])
                    # Calculate the MSE for each Gauss
                    ys_for_sim = [] # different from assign the value 
                    for g in range(X[:,0].size):
                        x_for_sim = X[g][0]
                        y_for_sim = multi_bimodal(
                            x_for_sim, gmm.weights_ , *params)
                        ys_for_sim.append(y_for_sim)
                    MSE = calculate_MSE(X[:,1].tolist(), ys_for_sim)
                    ySp.append(MSE)
                    xSp.append(index)
                    MSE_list.append(MSE)
                incre_index = counter_initial

                while(True):
                    if n_samples < incre_index+1:
                        dimension_min_with_params.append({key+"_gauss": num_with_params[min_index],"max":max(X[:,0]),"min":min(X[:,0])})
                        break
                    gmm = mixture.GaussianMixture(n_components=incre_index+1, covariance_type="diag", max_iter=100).fit(X)
                    list_params = []
                    list_params = zerolistmaker((incre_index+1)*3)
                    params = tuple(list_params)
                    simulated_y_sum = 0
                    for sub_index in range(incre_index+1):
                        list_params[sub_index*3] = gmm.means_[sub_index][0]
                        list_params[sub_index*3+1] = gmm.covariances_[sub_index][0]
                        list_params[sub_index*3+2] = simulated_height_normal_dist(gmm.means_[sub_index][0], gmm.means_[sub_index][0], math.sqrt(gmm.covariances_[sub_index][0]))*gmm.weights_[sub_index]
                        # print("simulated_height_normal_dist",list_params[sub_index*3+2]*gmm.weights_[sub_index])
                        simulated_y_sum += list_params[sub_index*3+2]*gmm.weights_[sub_index]
                    print("TRUEsimulated_y_sum",simulated_y_sum)
                    params = tuple(list_params)
                    num_with_params[incre_index] = list_params
                    # print(str(index+1),params,len(params))
                    # Calculate the MSE for each Gauss
                    ys_for_sim = [] # different from assign the value 
                    for g in range(X[:,0].size):
                        x_for_sim = X[g][0]
                        y_for_sim = multi_bimodal(
                            x_for_sim, gmm.weights_ , *params)
                        ys_for_sim.append(y_for_sim)
                    MSE = calculate_MSE(X[:,1].tolist(), ys_for_sim)
                    MSE_list.append(MSE)
                
                    # print(MSE_list)
                    # print("-----------------------------")
                    ySp.append(MSE)
                    print("MSE",MSE)
                    xSp.append(incre_index)


                    y_firsts = obtain_first_second(np.array(ySp),np.array(xSp),"first")
                    y_seconds = obtain_first_second(np.array(ySp),np.array(xSp),"second")
                    if(abs(y_seconds[-1]) < 0.1 or y_firsts[-1]>0 or incre_index==100):
                        
                        print("incre_index", incre_index)
                        # print("global_params", params)
                        print("ySp", ySp)
                        print("ySp.index(min(ySp))", ySp.index(min(ySp)))
                        min_index = ySp.index(min(ySp))
                        print("xSp",xSp)
                        # print("x_range",x_range)
                        y_firsts = obtain_first_second(np.array(ySp),np.array(xSp),"first")
                        y_seconds = obtain_first_second(np.array(ySp),np.array(xSp),"second")

                        print("y_seconds",y_seconds)
                        print("y_firsts",y_firsts)
                        super_global_params = params
                        break
                    incre_index += 1
                dimension_min_with_params["gauss"] = num_with_params[min_index]
                dimension_min_with_params["weights"] = num_with_weights[min_index]
                dimension_min_with_params["max"] = max(X[:,0])
                dimension_min_with_params["min"] = min(X[:,0])
                print("type(X[:,0])", type(X[:,0]))
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
                all_files_dimension_with_params[file[0:findNth(file,"_",2)]] = dimension_min_with_params
              
            
    with open(gauss_filetype+"_features_gauss.json", "w") as outfile:
        json.dump(all_files_dimension_with_params,outfile)


if __name__ == "__main__":

    main()
