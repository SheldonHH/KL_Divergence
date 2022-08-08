import pandas as pd
import csv
import time


def transpose_combine(combined_fullPath,target_transposePath):
    pd.read_csv(combined_fullPath, "rb", header=None).T.to_csv(
        target_transposePath, header=False, index=False)

def main():
    t0 = time.time()
    for idx in range(4096): 
      print("idx",idx)
      input_fullpath = "/home/xphuang/entropy/user_gauss_params/data/individual_features/feature_"+str(idx)+".csv"
      output_fullpath = "/home/xphuang/entropy/user_gauss_params/data/individual_features/T/transposed_"+str(idx)+".csv"
      transpose_combine(input_fullpath, output_fullpath)
    t1 = time.time()
    print(t1-t0)
    
    

if __name__ == "__main__":
    main()




import csv
