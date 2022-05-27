import numpy as np
# from sklearn.mixture import GaussianMixture
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

def read_from_csv(r_dense_trimmed_data_path1, w_freq_path):
    df = pd.read_csv(r_dense_trimmed_data_path1)
    write_to_json(df, w_freq_path)


def write_to_json(df, w_freq_path):
    json_file_to_write = open(w_freq_path, 'w')
    # json_file_to_write.write(json.dumps(df['x1'].value_counts().to_dict()))
    trimmed_dict = df.to_dict()
    freq_dict = {}
   
    for key, value in trimmed_dict.items():
        freq_dict[key] = pd.DataFrame.from_dict(
            value, orient='index').value_counts().to_dict()

        print("len",len(freq_dict[key]))
        # print(pd.DataFrame.from_dict(value, orient='index').value_counts())
    # print(freq_dict)

    final_col_freq_dict = {}
    for bigger_key, bigger_value in freq_dict.items():
        col_freq_dict = {}
        for key, value in bigger_value.items():
            col_freq_dict[key[0]] = value
        final_col_freq_dict[bigger_key] = col_freq_dict
    json_file_to_write.write(json.dumps(final_col_freq_dict))


def main():
    args = sys.argv[1:]
    print(args)
    # user_1_data
    raw_data_path1 = args[0]
    middle_index = args[0].rindex('/')
    last_index = len(args[0])-1
    first_half = args[0][0:middle_index+1]
    before_extension_half = args[0][middle_index+1: args[0].rindex('.')]
    r_dense_trimmed_data_path1 = first_half + \
        "trimmed/dense_trimmed_"+before_extension_half+".csv"
    w_freq_path = first_half + \
        "independent/freq_"+before_extension_half+".json"
    read_from_csv(r_dense_trimmed_data_path1, w_freq_path)

    with open(w_freq_path, 'r') as f:
        freq_dict = json.load(f)
    # print("freq_dict",freq_dict)



if __name__ == "__main__":

    main()
