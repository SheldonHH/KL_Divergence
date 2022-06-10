import pandas as pd
import sys

def main():
    args = sys.argv[1:]
    raw_csv_path1 = args[0]
    middle_index = args[0].rindex('/')
    last_index = len(args[0])-1
    lists = []
    path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    username = raw_csv_path1[raw_csv_path1.rindex('/')+1: raw_csv_path1.rindex('.')]
    # pd.DataFrame(features).to_csv(path+username+"_features.csv", header=False)
    df = pd.read_csv(path+"/features/rounded_"+username+'_features.csv', names=['col1'])
    print("df",df)
    print(df.value_counts())
    df.value_counts(normalize=True).to_csv(path+"/features/freq/"+username+"_freq.csv", header=False)

if __name__ == "__main__":
    main()

