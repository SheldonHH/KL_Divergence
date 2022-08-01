import numpy as np
import glob
import os
import csv
# import freq_to_gauss
import numpy as np
# from sklearn.mixture import GaussianMixture
# https://stackoverflow.com/a/35992526/5772735
import os
from pylab import *
from functools import reduce
from scipy.stats import norm
from sklearn import mixture
import time
import json
import csv
from MQ4C import *
from g_to_e import *
import math

# Creating a Function.
def simulated_height_normal_dist(x, mean, sd):
    return norm.cdf(x, mean, sd)

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


# simplied freq to gauss
def freq_to_gauss(true_datapath,  inputfile,  col_counter, raw_data_size, username, call_sign_folder):
    freq_dir = true_datapath+"/q/"+username+"/"
    uname = username
    os.chdir(freq_dir)
    # num_with_params = {}  # (num_of_gauss, [params])
    # num_with_weights = {}
    all_files_dimension_with_params = {}
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
        f.close()   


        gmm = mixture.GaussianMixture(
            n_components=1, covariance_type="diag", max_iter=500000).fit(X)
        list_params = zerolistmaker((1)*3)
        wmch = [[], [], [], []]  # weight, means, covariances, height

        wmch[0].append(gmm.weights_[0])
        wmch[1].append(gmm.means_[0][0])
        wmch[2].append(gmm.covariances_[0][0])
        simulated_height = simulated_height_normal_dist(gmm.means_[0][0], gmm.means_[0][0], math.sqrt(gmm.covariances_[0][0])) * gmm.weights_[0]
        wmch[3].append(simulated_height)
        wmch = np.array(list(map(list, zip(*wmch))))
        # wmch = wmch[wmch[:, 0].argsort(kind='mergesort')]  

        list_params[0*3] = wmch[0][1]
        list_params[0*3+1] = wmch[0][2]
        list_params[0*3+2] = wmch[0][3]
        # num_with_params[0] = list_params
        # num_with_weights[0] = [i[0] for i in wmch]

        minList = []
        maxList = []
        
        # dimension_min_with_params["weights"] = num_with_weights[0]
        dimension_min_with_params["weights"] = 1
        dimension_min_with_params["gauss"] = list_params
        minList, maxList = calculate_max_min(list_params)

        dimension_min_with_params["max"] = maxList
        dimension_min_with_params["min"] = minList
        dimension_min_with_params["raw_data_size"] = raw_data_size
        all_files_dimension_with_params[username +
                                        "_"+col_counter] = dimension_min_with_params
    counterFolder = true_datapath+"users_individual_gauss/"+call_sign_folder+"/"+ col_counter+"/"
    if os.path.isdir(counterFolder) == False:
        os.makedirs(counterFolder, exist_ok=True)
        for f in glob.glob(counterFolder+"*.csv"):
            os.remove(f)
    with open(counterFolder + uname+"_"+col_counter+"_gauss.json", "w") as outfile:
        json.dump(all_files_dimension_with_params, outfile)



# calculate max and min
def calculate_max_min(gaussList):
    minList = []
    maxList = []
    for sub_index in range(int(len(gaussList)/3)):
        mean = gaussList[sub_index*3] 
        sigma = gaussList[sub_index*3+1]
        ci = norm.interval(0.99, loc=mean, scale=sigma)
        minList.append(ci[0])
        maxList.append(ci[1])
    return minList, maxList
    

def raw_data_size(username):
    numpy_array = np.loadtxt(
        "/home/xphuang/entropy/user_gauss_params/data/q/"+username+"/"+username+"_0_q.csv", delimiter=",")
    return len(numpy_array)


def f_to_g(Dir, username, call_sign_folder):
    rds = raw_data_size(username)
    this_user_dir = Dir+"users_individual_gauss/"+username+"/"
    if os.path.isdir(this_user_dir) == False:
        os.mkdir(this_user_dir)  # make dir for that user
    for feat_counter in range(4096):
        print(username, "'s featureCounter", feat_counter)
        inputfile = Dir+"q/"+username+"/"+username+"_"+str(feat_counter)+"_q.csv"
        freq_to_gauss(Dir, inputfile, str(
            feat_counter), str(rds), username, call_sign_folder)
            

def main():
    Dir = "/home/xphuang/entropy/user_gauss_params/data/"
    sample_percent = 20
    Inputdicts = {"user_1": [1, 10000], "user_2": [10000, 20000], "user_3": [20000, 30000], "user_4": [30000,40000], "user_5": [40000,50000], "user_6": [50000,60000]}
    selected_users_set = set(Inputdicts.keys())

    # 1. generate Gauss for all users
    t0 = time.time()
    gauss_folder_ID = "one_gauss"
    for uname in Inputdicts.keys():
        f_to_g(Dir, uname, gauss_folder_ID)
    t1 = time.time()
    print("1. generate Gauss for all users: ",t1-t0)
 

    # 2. Consolidate Gauss for SELECTED users
    t0 = time.time()
    unite_gauss(selected_users_set, gauss_folder_ID)
    t1 = time.time()
    print("2. Consolidate Gauss for selected users takes process time: ",t1-t0)


    # 3. Generate Entropy from Gauss
    t0 = time.time()
    g_to_e(gauss_folder_ID, len(Inputdicts.keys()), sample_percent)
    t1 = time.time()
    print("3. g to e process time:",t1-t0)


if __name__ == "__main__":
    main()
