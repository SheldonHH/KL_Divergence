import csv
import sys
import pandas as pd
import os
import glob
# csv.field_size_limit(sys.maxsize)

username = "user_2"
for key in range(4096):
  print(key)
  input_nf_path = '/root/KL_Divergence/user_gauss_params/data/nofeatures/'+username+"/"+username+"_"+str(key)+'_onerow.csv'

  output_nf_path = '/root/KL_Divergence/user_gauss_params/data/nofeatures/'+username+"/"+username+"_"+str(key)+'_nf.csv'
  # pd.read_csv(input_nf_path, "rb", header=None).T.to_csv(output_nf_path, header=False, index=False)

  a = zip(*csv.reader(open(input_nf_path, "rt")))
  csv.writer(open(output_nf_path, "wt")).writerows(a)
  os.remove(input_nf_path)



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