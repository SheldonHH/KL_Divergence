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



    
# from tally import countFreq
def count_freq(true_arg_datapath, df, idx, username):
    # pd.DataFrame(features).to_csv(path+username+"_features.csv", header=False)
    # df = pd.read_csv(inputfile, names=['col1'])
    # print("df",df)
    print(df.value_counts())
    this_user_FreqDir = true_arg_datapath+"/q_freq/" + username + "/"
    if os.path.isdir(this_user_FreqDir) == False:
        os.mkdir(this_user_FreqDir)  # make dir for that user
    df.value_counts(normalize=True).to_csv( this_user_FreqDir+
                                           username+"_"+idx+"_freq.csv", header=False)
    # os.remove(path+"/features/rounded_"+username+'_features.csv')




# def cf_and_q(Dir, input_combine_file, username):
#     datafile = open(input_combine_file, 'r')
#     datareader = csv.reader(datafile, delimiter=' ')
#     data = []
#     counter = 0

#     transposed_inputs_list = glob.glob(input_combine_file+'*.{}'.format(extension))
#     sorted_files = natsort.natsorted(transposed_inputs_list)
#     all_filenames = [i for i in sorted_files]
#     for row in datareader:
#         print(counter)
#         print(len(row))
#         count_freq(Dir, pd.DataFrame(row), str(counter), username)
#         counter+=1
#         with open(target_fullPath, "w") as f:
#             for file in sorted_filenames:
#                 print(counterrr)
#                 counterrr+=1
#                 with open(file) as fff:
#                     f.write(fff.read())
    # df = pd.read_csv(input_combine_file)
    # # print(df)
    # print(len(df))
    # return
    # idx = 0
    # for column in df:
    #     print(idx)
    #     inputfile = input_combine_file+username+"_"+str(idx)+"_feature.csv"
    #     count_freq(Dir, df[column], str(idx), username)
    #     idx+=1
    
def adjust_field_size_limit():
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10 
        # as long as the OverflowError occurs.
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)


def cf_nf(Dir, input_combine_file, target_path, username):
    datafile = open(input_combine_file, 'r')
    datareader = csv.reader(datafile, delimiter=' ')
    data = []
    sorted_filenames = []
    for i in range(4096):
        sorted_filenames.append(target_path+username+"_"+str(i)+".csv")
    
    counter = 0
    for row in datareader:
        print(counter)
        with open(sorted_filenames[counter],'w') as f:
            writer = csv.writer(f)
            writer.writerow(row)
            # for val in row:
            #     writer.writerow([val])

def main():
    adjust_field_size_limit()
    t0 = time.time()
    username = "user_1"
    Dir = "/root/KL_Divergence/user_gauss_params/data/"
    input_combine_file = "/root/KL_Divergence/user_gauss_params/data/combine/transposed_"+username+"_comnbined.csv"
    target_path = "/root/KL_Divergence/user_gauss_params/data/nofeatures/"+username+"/"
    ####
    cf_nf(Dir,input_combine_file,target_path,username) # calculate Frequency
    ####
    t1 = time.time()
    print(t1-t0)

    # raw_csv_path1 = psedo_user_dir
    # username = raw_csv_path1[raw_csv_path1.rindex(
    #     '/')+1: raw_csv_path1.rindex('.')]
    # # cf_and_q(Dir, psedo_user_dir, username)
    # f_to_g(Dir, psedo_user_dir, username)
    # inputfile = Dir + 'combine/combined_features.csv'
    # df = pd.read_csv(inputfile, header=None).T
    # for index, row in df.iterrows():
    #     countFreq(raw_csv_argv, row)


if __name__ == "__main__":
    main()
