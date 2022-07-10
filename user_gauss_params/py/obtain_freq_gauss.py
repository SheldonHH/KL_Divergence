from this import d
import pandas as pd
import numpy as np
import glob
import os
import csv
import re
import natsort
from tally import countFreq


def main():
    Dir = "/root/KL_Divergence/user_gauss_params/data/"
    psedo_user_dir = "/root/KL_Divergence/user_gauss_params/data/user_4.csv"
    
    inputfile = Dir + 'combine/combined_features.csv'
    df = pd.read_csv(inputfile, header=None).T
    for index, row in df.iterrows():
        countFreq(raw_csv_argv, row)


if __name__ == "__main__":
    main()
