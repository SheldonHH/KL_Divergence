from this import d
import pandas as pd
import numpy as np
import glob
import os
import csv
import re
import natsort
import time
# from tally import countFreq
# from itertools import izip

# setting the path for joining multiple files
# files = os.path.join("/root/KL_Divergence/user_gauss_params/data/features/", "*.csv")

# # list of merged files returned
# files = glob.glob(files)

# print("Resultant CSV after joining all CSV files at a particular location...");

# # joining files with concat and read_csv
# df = pd.concat(map(pd.read_csv, files), ignore_index=True)
# print(df)
# df.to_csv("/root/KL_Divergence/user_gauss_params/data/combine/combined_features.csv",index=False)
# df.value_counts(normalize=True).to_csv(path+"/features/freq/"+username+"_freq.csv", header=False)


# def transpose_csv(Dir):
#     csv_file_list = glob.glob(Dir + 'features/*.csv')
#     counter = 0
#     for file in csv_file_list:
#         a = zip(*csv.reader(open(file, "rt")))
#         csv.writer(open(Dir+'transposed_features/user_4_' +
#                    str(counter)+".csv", "wt")).writerows(a)
#         counter += 1


# def t_and_freq(Dir):
#     inputfile = Dir + 'combine/combined_features.csv'
#     df = pd.read_csv(inputfile, header=None).T
#     for index, row in df.iterrows():
#         print("row", row)
#         count_freq(raw_csv_argv, row)

# for each id_feature
# generate one gauss
# def i_and_freq(Dir):
#     for feat_counter in range(4096):
#         inputfile =  Dir+"/nofeatures/"+str(feat_counter)+"_feature.csv"
#         countFreq(Dir, feat_counter)





        


# def transpose_combine(Dir):
#     inputfile = Dir + 'combine/combined_features.csv'
#     outputfile = Dir+'combine/transposed_combined_features.csv'
#     # a = zip(*csv.reader(open(file, "rt")))
#     # csv.writer(
#     #     open(Dir+'combine/transposed_combined_features.csv', "wt")).writerows(a)
#     pd.read_csv(inputfile, header=None).T.to_csv(
#         outputfile, header=False, index=False)
    # return 

def perform_combine(transposed_inputs_dir, target_dir):
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
   #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f)+"\n" for f in all_filenames ])
   #export to csv
    combined_csv.to_csv( target_dir, index=False, encoding='utf-8-sig')

# def perform_split_by_col(transposed_inputs_dir, target_dir):
#     extension = 'csv'
#     all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#    #combine all files in the list
#     combined_csv = pd.concat([pd.read_csv(f)+"\n" for f in all_filenames ])
#    #export to csv
#     combined_csv.to_csv( target_dir, index=False, encoding='utf-8-sig')


def main():
    t0 = time.time()
    Dir = "/root/KL_Divergence/user_gauss_params/data/"
    username = "user_1"
    transposed_inputs_dir = "/root/KL_Divergence/user_gauss_params/data/transposed_features/"+username+"/"
    target_dir = "/root/KL_Divergence/user_gauss_params/data/combine/"+username+"_comnbined.csv"
    perform_combine(transposed_inputs_dir,target_dir)

    t1 = time.time()
    print(t1-t0)
    # i_and_freq(Dir)


 
    # for tfile in transposed_eachuser:
    #     user_filename = tfile[tfile.rindex('/')+1: tfile.rindex('.')]
    #     with open(file) as rf:


    # Write one feature file, total feature: 4096
    # read all user file
 

    # afters = zip(*befores)    
    # # for row in afters:
    # print(afters)
    # csv.writer(open(Dir+'combine/transposed_combined_features.csv', "wt")).writerows(afters)       
    # print(befores)
    # countFreq([psedo_user_dir], np.array(befores).T[0], 0)
    # for idx,row in enumerate(np.array(befores).T):
    #     count_freq([psedo_user_dir], row,idx)
    #     if idx == 0:
    #         break

    # transpose_combine(Dir)

    # t_and_freq(Dir)

if __name__ == "__main__":
    main()
