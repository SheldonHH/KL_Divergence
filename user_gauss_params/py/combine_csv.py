import pandas as pd
import glob
import os
import csv
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

def transpose_csv(Dir):
  csv_file_list = glob.glob(Dir + 'features/*.csv')
  counter = 0
  for file in csv_file_list:
    a = zip(*csv.reader(open(file, "rt")))
    csv.writer(open(Dir+'transposed_features/user_4_'+str(counter)+".csv", "wt")).writerows(a)
    counter+=1

def main():
  Dir = "/root/KL_Divergence/user_gauss_params/data/"
  # transpose_csv(Dir)
  csv_file_list = glob.glob(Dir + 'transposed_features/*.csv')
  with open(Dir+"combine/" + 'combined_features.csv','w') as wf:
      for file in csv_file_list:
          with open(file) as rf:
              for line in rf:
                  if line.strip(): # if line is not empty
                      if not line.endswith("\n"):
                          line+="\n"
                      wf.write(line)

if __name__ == "__main__":
    main()
