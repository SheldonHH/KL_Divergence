import pandas as pd
import time

def main():
    # 0. Load combined_features.csv
    t0 = time.time()
    location_of_combined_file = "/home/xphuang/entropy/user_gauss_params/data/combine/" + "user_2_comnbined.csv"
    df = pd.read_csv(location_of_combined_file,  delimiter=" ")
    t1 = time.time()
    print("Step 0: loading combined.csv takes: ", t1-t0)


    # 1.Split to multiple files
    t0 = time.time()
    col_counter = 0
    for col in df.columns:
        print("col_counter:",col_counter)
        df[col].to_csv(f'/home/xphuang/entropy/user_gauss_params/data/individual_features/feature_{col_counter}.csv', index=False, header=False)
        col_counter+=1

    t1 = time.time()
    print("Step 1: Split to multiple files: ", t1-t0)

if __name__ == "__main__":
    main()
