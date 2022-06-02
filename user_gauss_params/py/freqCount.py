import pandas as pd
lists = []

df = pd.read_csv('/root/KL_Divergence/user_gauss_params/data/uniform/user_4.txt')
df.value_counts().to_csv("/root/KL_Divergence/user_gauss_params/data/uniform/freq/trimmed_user_4_freq.csv", header=False)