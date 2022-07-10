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





        


def transpose_combine(Dir):
    inputfile = Dir + 'combine/combined_features.csv'
    outputfile = Dir+'combine/transposed_combined_features.csv'
    # a = zip(*csv.reader(open(file, "rt")))
    # csv.writer(
    #     open(Dir+'combine/transposed_combined_features.csv', "wt")).writerows(a)
    pd.read_csv(inputfile, header=None).T.to_csv(
        outputfile, header=False, index=False)
    # return 

# def perform_combine(Dir):
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



def transpose_csv(Dir, username):
    input_file_list = glob.glob(Dir + 'features/'+username+"/*.csv")
    # print(input_file_list)
    counter = 0
    for inputfile in input_file_list:
        outputfile = Dir+'transposed_features/'+ username  +'/transposed_'+ username + "_"+str(counter)+".csv"
        a = zip(*csv.reader(open(inputfile, "rt")))
        csv.writer(open(outputfile, "wt")).writerows(a)
                # open(Dir+'combine/transposed_combined_features.csv', "wt")).writerows(a)
        # pd.read_csv(inputfile, header=None).T.to_csv(outputfile, header=False, index=False)
        counter += 1

def create_nofeature(transposed_eachuser,Dir,username):
    for feat_counter in range(4096):
        if os.path.exists(Dir+"nofeatures/"+username+"/"+username+"_"+str(feat_counter)+"_feature.csv") == False:
            with open(Dir+"nofeatures/"+username+"/"+username+"_"+str(feat_counter)+"_feature.csv","w") as wf:
                for file in transposed_eachuser:
                    with open(file) as rf:
                        for line in rf:
                            li = list(line.split(" "))
                            if feat_counter < len(li):
                                wf.write(li[feat_counter]+"\n")

def main():
    t0 = time.time()
    Dir = "/root/KL_Divergence/user_gauss_params/data/"
    username = "user_1"
    psedo_user_dir = "/root/KL_Divergence/user_gauss_params/data/"+username+".csv"
    ## transpose individual csv
    # output_specified_dir = Dir + 'transposed_features/'+username
    # if os.path.isdir(output_specified_dir) == False:
    #     os.mkdir(output_specified_dir)
    # transpose_csv(Dir,username)

    ## from transposed_csv to freq
    output_specified_dir = Dir + 'nofeatures/'+username
    if os.path.isdir(output_specified_dir) == False:
        os.mkdir(output_specified_dir)
    transposed_eachuser = glob.glob(Dir + 'transposed_features/'+username+'/*.csv')
    create_nofeature(transposed_eachuser,Dir,username)
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
