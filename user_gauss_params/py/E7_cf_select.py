import pandas as pd
import time
import pandas as pd
import random
dicts = {"user_1": [1, 30], "user_2": [3, 60], "user_3": [70, 800]}
t0 = time.time()
df = pd.read_csv("/home/xphuang/entropy/user_gauss_params/data/combine/user_2_comnbined.csv", delimiter=" ")
t1 = time.time()
print("readcsv time:",t1-t0)
# dfRange = df.iloc[start:end]
# value:[]

t0 = time.time()
xi_dict = {}
xi_list = []
total_rows = 0
for key, value in dicts.items():
    dfRange = df.iloc[value[0]:value[1]]
    print(len(dfRange))
    xi_dict[key] = (dfRange.agg([min, max]), len(dfRange))
    total_rows+=len(dfRange)
    
    xi_list.append(dfRange.agg([min, max]))
    # print(dfRange.agg([min, max]))
    # print("individual size",len(dfRange))

    dfRange.to_csv("/home/xphuang/KL_Divergence/user_gauss_params/data/combine/" +
                   key+"_combined.csv", header=False, index=False)
    # df.agg([min, max])

result = pd.concat(xi_list)
# print("total size",len(result))
# print(result.agg([min, max]))
total_size = total_rows
print(total_size)
print("$$$$$$$$$$$$$$$$$$$$$")
print(total_rows)
t1 = time.time()
print("generate file time:",t1-t0)
t0 = time.time()
data4=df.iloc[[1,20],[0]]
print(data4)
t1 = time.time()
print("iloc time:",t1-t0)