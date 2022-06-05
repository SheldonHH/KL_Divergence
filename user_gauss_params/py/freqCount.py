import pandas as pd
lists = []

df = pd.read_csv('/root/KL_Divergence/user_gauss_params/data/uneven/features/rounded_user_4_features.csv', names=['col1'])
# df.columns = ['col1']
print("df",df)
# sg = df.T
# sg.columns =  ['col1']
# # sg.sort_values(by='col1')
# print('sg',sg)
print(df.value_counts())
df.value_counts(normalize=True).to_csv("/root/KL_Divergence/user_gauss_params/data/uneven/features/freq/user_4_freq.csv", header=False)