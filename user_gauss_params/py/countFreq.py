import pandas as pd
import sys
import os
# class count_freq:
def count_freq(raw_csv_argv, inputfile, idx):
    args = raw_csv_argv
    raw_csv_path1 = args[0]
    path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    username = raw_csv_path1[raw_csv_path1.rindex('/')+1: raw_csv_path1.rindex('.')]
    # pd.DataFrame(features).to_csv(path+username+"_features.csv", header=False)
    df = pd.read_csv(inputfile, names=['col1'])
    # print("df",df)
    print(df.value_counts())
    df.value_counts(normalize=True).to_csv(path+"/q_freq/"+username+"_"+idx+"_freq.csv", header=False)
    # os.remove(path+"/features/rounded_"+username+'_features.csv')

