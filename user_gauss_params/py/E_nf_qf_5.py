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
def count_freq(true_arg_datapath, output_q_file, df, idx, username):
    # pd.DataFrame(features).to_csv(path+username+"_features.csv", header=False)
    # df = pd.read_csv(inputfile, names=['col1'])
    # print("df",df)
    print(df.value_counts())
    if os.path.isdir(output_q_file) == False:
        os.mkdir(output_q_file)  # make dir for that user
    df.value_counts(normalize=True).to_csv( output_q_file+
                                           username+"_"+idx+"_freq.csv", header=False)
    # os.remove(path+"/features/rounded_"+username+'_features.csv')



def i_and_freq(Dir, input_nf_file, output_q_file, username):
    csv_file_list = glob.glob(input_nf_file+'/*.csv')
    for file in csv_file_list:
        df = pd.read_csv(file)
        count_freq(Dir, output_q_file, df, str(idx), username)
    

def main():
    t0 = time.time()
    username = "user_1"
    Dir = "/root/KL_Divergence/user_gauss_params/data/"
    # input_combine_file = "/root/KL_Divergence/user_gauss_params/data/combine/"+username+"_comnbined.csv"
    input_nf_file = Dir+"nofeature/"+username + "/"
    output_q_file =  Dir+"q_freq/"+username + "/"
    ####
    i_and_freq(Dir,input_nf_file, output_q_file, username) # calculate Frequency
    ####
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
