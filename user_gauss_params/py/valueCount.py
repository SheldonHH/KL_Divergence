import pandas as pd
lists = []

with open('/root/KL_Divergence/user_gauss_params/data/uneven/user_4.txt') as f:
    line = f.readline()
    while line:
        line = f.readline()
        if line != '':
          lists.append(float(line))

x=pd.Series(lists)


x.value_counts().to_csv("/root/KL_Divergence/user_gauss_params/data/uneven/trimmed_user_4_freq.csv", header=False)