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


def main():
    num_of_slides = 10
    uneven_dir = "/root/KL_Divergence/user_gauss_params/data/uneven/features"
    uniform_dir = "/root/KL_Divergence/user_gauss_params/data/uniform/features"
    dir_str = uniform_dir
    gauss_filetype = "uneven"

       # load sample_gauss
    sample_gauss = {}
    os.chdir(dir_str+"/")
    cwd = os.getcwd()
    print("Current working directory is:", cwd)
    sample_data_directory = os.path.join(dir_str+"/")
    # DON"T USE os.walk
    for item in os.listdir(dir_str):
        if os.path.isfile(os.path.join(dir_str, item)) and item.endswith('.json'):
            print(item)
            f=open(item)
            data = json.load(f)
            for uname, user in data.items():
                sample_gauss[uname] = user["gauss"]
            f.close()

    all_population_gauss = {}
    os.chdir(dir_str+"/freq/")
    cwd = os.getcwd()
    print("Current working directory is:", cwd)
    # DON"T USE os.walk
    for item in os.listdir(dir_str+"/freq/"):
        if os.path.isfile(os.path.join(dir_str+"/freq/", item)) and item.endswith('.json'):
            print(item)
            f=open(item)
            data = json.load(f)
            print("data",data)
            for uname, user in data.items():
                all_population_gauss[uname] = user["gauss"]
            f.close()
    print("all_population",all_population_gauss)
    
    user_distance_map = {}
    for key,value in all_population_gauss.items(): 
      dimen_distance_array = []
      print("len(value)",len(value))
      for inx in range(0,len(value),3):
        population_mean = value[inx]
        population_cov = value[inx+1]
        sample_mean = sample_gauss[key][inx]
        sample_cov = sample_gauss[key][inx+1]
        distance = abs(population_mean-sample_mean)-(sqrt(population_cov)+sqrt(sample_cov))
        dimen_distance_array.append(distance>0)
        if distance<0:
          print("distance check fail")
      user_distance_map[key]=dimen_distance_array
    
    print(user_distance_map)
    # write_dict_to_json(user_distance_map, "population_sample_map.json")
             
            
if __name__ == "__main__":

    main()
