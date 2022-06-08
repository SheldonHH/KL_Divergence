import numpy as np
# from sklearn.mixture import GaussianMixture
# https://stackoverflow.com/a/35992526/5772735
from curses import raw
from ntpath import join
from re import S
import os
from pylab import *
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
import plt_freq_to_gaussian
from random import sample
from functools import reduce

def write_dict_to_json(dict, json_to_write):
    df_params = pd.DataFrame.from_dict(dict)
    result = df_params.to_json(orient="columns")
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))

def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)

def sample_subportion(subportion, percent_in_decimal):
  sample_size = int(len(subportion) * percent_in_decimal )
  if sample_size > 0:
    sample_list = sample(subportion,sample_size)
    print("sample_size", sample_size)
  else:
    sample_list = sample(subportion,1)
    print("sample_size", sample_size)
  return sample_list

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

def simulated_height_normal_dist(x, mean, sd):
    return norm.cdf(x, mean, sd)

def main():
    num_of_slides = 10
    uneven_dir = "/root/KL_Divergence/user_gauss_params/data/uneven/features/"
    uniform_dir = "/root/KL_Divergence/user_gauss_params/data/uniform/features/"
    dir_str = uneven_dir
    gauss_filetype = "uneven"

    num_with_params = {}
    all_files_dimension_with_params = {}

    all_population_gauss = {}
    freq_directory = os.path.join(dir_str+"freq")
    os.chdir(dir_str+"freq")   
    for root,dirs,files in os.walk(freq_directory):
      for file in files:
        if file.endswith(".json"):
              f=open(file, 'r')
              population_gauss = json.load(f)
              print('len=-----',len(population_gauss))
              for uname, user in population_gauss.items():
                  # print(len(user["gauss"][0])/3)
                  print("uname",uname)
                  all_population_gauss[uname]=user["gauss"]
    sample_data_directory = os.path.join(dir_str)
    os.chdir(dir_str)   
    file_gauss_dict = {}
    for root,dirs,files in os.walk(sample_data_directory):
        for file in files:
            dimension_min_with_params = {}
            if file.endswith(".json"):
                f=open(file, 'r')
                gaussNum=int(len(all_population_gauss[file[findNth(file,"_",1)+1:findNth(file,"_",3)]])/3)
                print("value_counts(np.array(theuser_sample))",type(pd.Series(np.array(theuser_sample)).value_counts().to_numpy()))
                # ready_for_gmm = np.array(theuser_sample)

                # ready_for_gmm = np.random.rand(len(theuser_sample),len(theuser_sample))

                # ready_for_gmm = np.zeros((2,len(theuser_sample)))
                # ready_for_gmm[0:,] = np.array(theuser_sample)
                # print("France",pd.Series(np.array(theuser_sample)).value_counts(normalize=True, sort=True))
                sgg = list(pd.Series(np.array(theuser_sample)).value_counts(normalize=True, sort=True))
                # print("sggggg",sgg)


                ready_for_gmm = np.c_[np.unique(np.array(theuser_sample), return_counts=1)]
                # print("ready_for_gmm: ",ready_for_gmm)
                # np.append(np.array(theuser_sample),pd.Series(np.array(theuser_sample)).value_counts().to_numpy())
                # print("pd.Series(np.array(theuser_sample)).value_counts().to_numpy()",pd.Series(np.array(theuser_sample)).value_counts().to_numpy())
                print("gaussNumgaussNumgaussNum",gaussNum)
                gmm = mixture.GaussianMixture(n_components=gaussNum, covariance_type="diag", max_iter=500000).fit(ready_for_gmm)
                gauss_weights_dict = {}
                sample_params = []
                sample_params = zerolistmaker(gaussNum*3)
                simulated_y_sum = 0
                for sub_index in range(gaussNum):
                    sample_params[sub_index*3] = gmm.means_[sub_index][0]
                    sample_params[sub_index*3+1] = gmm.covariances_[sub_index][0]
                    sample_params[sub_index*3+2] = simulated_height_normal_dist(gmm.means_[sub_index][0], gmm.means_[sub_index][0], math.sqrt(gmm.covariances_[sub_index][0]))*gmm.weights_[sub_index]
                # print("sample_params", sample_params)  
                gauss_weights_dict["gauss"] = sample_params
                gauss_weights_dict["weights"] = gmm.weights_.tolist()
                file_gauss_dict[file[findNth(file,"_",1)+1:findNth(file,"_",3)]] = gauss_weights_dict
        print("file_gauss_dict",file_gauss_dict)
        write_dict_to_json(file_gauss_dict, gauss_filetype+"_sample_gauss.json")
                
                
                
             
            
if __name__ == "__main__":

    main()
