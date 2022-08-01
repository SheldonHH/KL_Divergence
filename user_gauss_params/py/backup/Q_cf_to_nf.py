import pandas as pd

df = pd.read_csv('/home/xphuang/entropy/user_gauss_params/data/combine/user_2_comnbined.csv', delimiter=" ", header=None)
counter = 0
print(df.shape[1])
for idx in range(df.shape[1]):
#     # print(colname, colval.values)
    print(counter)
    df[idx].to_csv('/home/xphuang/entropy/user_gauss_params/data/nofeatures/feat_separated_file/'+str(counter)+".csv", header=False, index=False)
    counter+=1