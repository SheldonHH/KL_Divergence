import pandas as pd
df = pd.read_csv('/root/KL_Divergence/user_gauss_params/data/combine/user_1_comnbined.csv')
counter = 0
print(df.info())
print(df.head())
print(df.describe())
# print(df.columns)
# dList = df.to_numpy()
# print(df)
# print(len(df.to_numpy()))
# for row in df.to_numpy():
#     print(counter)
#     counter+=1