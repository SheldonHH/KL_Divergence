from this import d
import pandas as pd
import numpy as np
import glob
import os
import csv
import re
import natsort
import time


def transpose_combine(combined_fullPath,target_transposePath):
    # a = zip(*csv.reader(open(file, "rt")))
    # csv.writer(
    #     open(Dir+'combine/transposed_combined_features.csv', "wt")).writerows(a)
    pd.read_csv(combined_fullPath, "rb", header=None).T.to_csv(
        target_transposePath, header=False, index=False)
    # return 

def main():
    t0 = time.time()
    Dir = "/root/KL_Divergence/user_gauss_params/data/"
    username = "user_1"
    # transposed_inputs_dir = "/root/KL_Divergence/user_gauss_params/data/transposed_features/"+username+"/"
    combined_fullPath = "/root/KL_Divergence/user_gauss_params/data/combine/"+username+"_comnbined.csv"
    target_transpose = "/root/KL_Divergence/user_gauss_params/data/combine/transposed_"+username+"_comnbined.csv"
    # perform_combine(transposed_inputs_dir,target_fullPath, username)
    transpose_combine(combined_fullPath, target_transpose)
    t1 = time.time()
    print(t1-t0)
    
    

if __name__ == "__main__":
    main()
