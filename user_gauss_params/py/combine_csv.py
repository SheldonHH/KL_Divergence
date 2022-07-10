from this import d
import pandas as pd
import glob
import os
import csv
import re
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
        outputfile = Dir+'transposed_features/'+ user_filename  +"_transposed.csv"
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


# def calculate_gauss():

# numbers = re.compile(r'(\d+)')
# def numericalSort(value):
#     parts = numbers.split(value)
#     parts[1::2] = map(int, parts[1::2])
#     return parts

def main():
    Dir = "/root/KL_Divergence/user_gauss_params/data/"
    # transpose individual csv
    transpose_csv(Dir)
    
    # csv_file_list = glob.glob(Dir + 'transposed_features/*.csv')
    # # print(csv_file_list)
    # # csv_file_list.sort()
    # # print(sorted(csv_file_list))
    # csv_file_list.sort(key=lambda f: int(re.sub('\D', '', f)))
    # print(csv_file_list)
    # with open(Dir+'combine/combined_features.csv', 'w') as wf:
    #     for file in csv_file_list:
    #         with open(file) as rf:
    #             for line in rf:
    #                 if line.strip():  # if line is not empty
    #                     if not line.endswith("\n"):
    #                         line += "\n"
    #                     wf.write(line)

    # transpose_combine(Dir)


if __name__ == "__main__":
    main()
