from this import d
import pandas as pd
import numpy as np
import glob
import os
import csv
import re
import natsort
from tally import countFreq
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

def transpose_csv(Dir):
    input_file_list = glob.glob(Dir + 'features/*.csv')
    # input_file_list.sort(key=lambda f: int(re.sub('\D', '', f)))
    
    counter = 0
    for inputfile in input_file_list:
        user_filename = inputfile[inputfile.rindex('/')+1: inputfile.rindex('.')]
        outputfile = Dir+'transposed_features/transposed_'+ user_filename  +".csv"
        a = zip(*csv.reader(open(inputfile, "rt")))
        csv.writer(open(outputfile, "wt")).writerows(a)
                # open(Dir+'combine/transposed_combined_features.csv', "wt")).writerows(a)
        
        # pd.read_csv(inputfile, header=None).T.to_csv(outputfile, header=False, index=False)
        counter += 1


def transpose_combine(Dir):
    inputfile = Dir + 'combine/combined_features.csv'
    outputfile = Dir+'combine/transposed_combined_features.csv'
    # a = zip(*csv.reader(open(file, "rt")))
    # csv.writer(
    #     open(Dir+'combine/transposed_combined_features.csv', "wt")).writerows(a)
    pd.read_csv(inputfile, header=None).T.to_csv(
        outputfile, header=False, index=False)
    # return 

# def calculate_gauss():

# numbers = re.compile(r'(\d+)')
# def numericalSort(value):
#     parts = numbers.split(value)
#     parts[1::2] = map(int, parts[1::2])
#     return parts

def main():
    Dir = "/root/KL_Divergence/user_gauss_params/data/"
    psedo_user_dir = "/root/KL_Divergence/user_gauss_params/data/user_4.csv"
    # transpose individual csv
    # transpose_csv(Dir)
    
    # #
    transposed_eachuser = glob.glob(Dir + 'transposed_features/*.csv')
    # print(transposed_eachuser)
    # print(csv_file_list)
    # csv_file_list.sort()
    # print(sorted(csv_file_list))
    # transposed_eachuser.sort(key=lambda f: int(re.sub('\D', '', f)))
    # transposed_eachuser.sort(key=lambda f: int(re.sub('\D', '', f)))
    # transposed_eachuser.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    # transposed_eachuser = natsort.natsorted(transposed_eachuser)
    # print(transposed_eachuser)
    # befores = []
    # with open(Dir+'combine/combined_features.csv', 'w') as wf:
    #     for file in transposed_eachuser:
    #         with open(file) as rf:
    #             for line in rf:
    #                 if line.strip():  # if line is not empty
    #                     if not line.endswith("\n"):
    #                         line += "\n"
    #                     wf.write(line) # type string
    #                     li = list(line.split(" ")) 
    #                     befores.append(li)
    #                     print(type(line))



 
    # for tfile in transposed_eachuser:
    #     user_filename = tfile[tfile.rindex('/')+1: tfile.rindex('.')]
    #     with open(file) as rf:


    # Write one feature file, total feature: 4096
    # read all user file
    for feat_counter in range(4096):
        with open(Dir+"nofeatures/"+str(feat_counter)+"_feature.csv","w") as wf:
            for file in transposed_eachuser:
                with open(file) as rf:
                    for line in rf:
                        li = list(line.split(","))
                        wf.write(li[feat_counter]+"\n")

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
    # inputfile = Dir + 'combine/combined_features.csv'
    # df = pd.read_csv(inputfile, header=None).T
    # for index, row in df.iterrows():
    #     print("row", row)
    #     count_freq(raw_csv_argv, row)


if __name__ == "__main__":
    main()
