from this import d
import pandas as pd
import numpy as np
import glob
import os
import csv
import re
import natsort
import time

def newline_combine(transposed_inputs_dir, target_fullPath, username):
    extension = 'csv'
    transposed_inputs_list = glob.glob(transposed_inputs_dir+'*.{}'.format(extension))
    sorted_files = natsort.natsorted(transposed_inputs_list)
    all_filenames = [i for i in sorted_files]
    print(len(all_filenames))
    csv_list = []
    counterrr = 0
    sorted_filenames = natsort.natsorted(all_filenames)
    with open(target_fullPath, "w") as f:
        for file in sorted_filenames:
            print(counterrr)
            counterrr+=1
            with open(file) as fff:
                f.write(fff.read())
        # csv_merged = pd.concat(csv_list, ignore_index=True)

# 6. Single DF is saved to the path in CSV format, without index column
    # csv_merged.to_csv(target_fullPath, index=False)

# def perform_combine(transposed_inputs_dir, target_fullPath, username):
#     extension = 'csv'
#     all_filenames = [i for i in glob.glob(transposed_inputs_dir+'*.{}'.format(extension))]
#     print(len(all_filenames))
#     csv_list = []
#     counterrr = 0
#     sorted_filenames = natsort.natsorted(all_filenames)
#     for file in sorted_filenames:
#         print(counterrr)
#         csv_list.append(pd.read_csv(file).assign(File_Name = os.path.basename(file)))
#         csv_list.append("\n")
#         counterrr+=1
#     csv_merged = pd.concat(csv_list, ignore_index=True)

# # 6. Single DF is saved to the path in CSV format, without index column
#     csv_merged.to_csv(target_fullPath, index=False)

   #combine all files in the list
#     combined_csv = pd.concat([pd.read_csv(f)+"\n" for f in all_filenames ])
#    #export to csv
#     combined_csv.to_csv( target_fullPath, index=False, encoding='utf-8-sig')

# def perform_split_by_col(transposed_inputs_dir, target_fullPath):
#     extension = 'csv'
#     all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#    #combine all files in the list
#     combined_csv = pd.concat([pd.read_csv(f)+"\n" for f in all_filenames ])
#    #export to csv
#     combined_csv.to_csv( target_fullPath, index=False, encoding='utf-8-sig')


def main():
    t0 = time.time()
    Dir = "/root/KL_Divergence/user_gauss_params/data/"
    username = "user_1"
    transposed_inputs_dir = "/root/KL_Divergence/user_gauss_params/data/transposed_features/"+username+"/"
    target_fullPath = "/root/KL_Divergence/user_gauss_params/data/combine/"+username+"_comnbined.csv"
    # perform_combine(transposed_inputs_dir,target_fullPath, username)
    newline_combine(transposed_inputs_dir,target_fullPath, username)
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
