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
from random import sample


def sample_subportion(subportion, percent_in_decimal):
  sample_size = int(len(subportion) * percent_in_decimal )
  if sample_size > 0:
    sample_list = sample(subportion,sample_size)
    print("sample_size", sample_size)
  else:
    sample_list = sample(subportion,1)
    print("sample_size", sample_size)
    return sample_list
  
def main():
    num_of_slides = 10
    uneven_dir = "/root/KL_Divergence/user_gauss_params/data/uneven/features/"
    uniform_dir = "/root/KL_Divergence/user_gauss_params/data/uniform/features/"
    dir_str = uniform
    directory = os.path.join(dir_str)
    os.chdir(dir_str)   
    num_with_params = {}
    all_files_dimension_with_params = {}
    for root,dirs,files in os.walk(directory):
        for file in files:
            dimension_min_with_params = {}
            if file.endswith(".csv") and file.startswith("rounded"):
                f=open(file, 'r')
                data_iter = csv.reader(f)
                data = [data for data in data_iter]
                unsorted_list = []
                for item in data:
                    unsorted_list.append(float(item[0]))
                unsorted_list.sort()
                # print("unsorted_list", unsorted_list)
                sorted_list = unsorted_list
                X = np.array(sorted_list)
                f.close()
                lmin = min(sorted_list)
                lmx = max(sorted_list)
                llen = len(sorted_list)
                step = (lmx-lmin)/num_of_slides 
                pos = lmin
                while(pos+step<lmx):
                    lower_bound = pos
                    upper_bound = pos + step
                    sub_portion = []
                    for item in sorted_list:
                      if item >= lower_bound and item < upper_bound and pos != lmx-step-step:
                        sub_portion.append(item)
                      if item >= lower_bound and item <= lmx and pos == lmx-step-step:
                        upper_bound = lmx
                        print("upper_bound",upper_bound)
                        sub_portion.append(item)
                    percent_in_decimal = 0.1
                    # print(file,lower_bound,"-",upper_bound,": ","before sample size",len(sub_portion),'min',min,'-max',lmx)
                    # print(sample_subportion(sub_portion, percent_in_decimal))
                    pos += step
                
                    
                 
                
                
                
             
            
if __name__ == "__main__":

    main()
