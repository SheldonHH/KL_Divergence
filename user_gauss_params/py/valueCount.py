import pandas as pd
lists = []

with open('/root/KL_Divergence/user_gauss_params/data/uniform/user_1.txt') as f:
    line = f.readline()
    while line:
        line = f.readline()
        if line != '':
          lists.append(float(line))

x=pd.Series(lists)


x.value_counts().to_csv("sg.csv", header=False)