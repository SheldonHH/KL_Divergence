# features
#


#       0,1,2,3,4,5,6,7,8,9
#  u1   1
#  u2 

import numpy as np
import pandas as pd
import time
# import random
# dicts = {"user_1": [0, 30], "user_2": [3, 60], "user_3": [70, 140]}
# df = pd.read_csv(
#     "/home/xphuang/entropy/user_gauss_params/data/combine/space_small_q.csv", delimiter=" ")

dicts = {"user_1": [1, 10000], "user_2": [10000, 20000], "user_3": [20000, 30000], "user_4": [30000,40000], "user_5": [40000,50000], "user_6": [50000,60000]}
df = pd.read_csv(
    "/home/xphuang/entropy/user_gauss_params/data/combine/user_2_comnbined.csv", delimiter=" ")


# dfRange = df.iloc[start:end]
# value:[]
user_dict = {}
xi_dict = {}
xi_list = []


# 1. Generate combined file for each user, read and write
t0 = time.time()
total_rows = 0
for key, value in dict(sorted(dicts.items())).items():
    dfRange = df.iloc[value[0]:value[1]]
    print(len(dfRange))
    user_dict[key] = dfRange
    xi_dict[key] = (dfRange.agg([min, max]), len(dfRange))
    total_rows+=len(dfRange)
    xi_list.append(dfRange.agg([min, max]))
    dfRange.to_csv("/home/xphuang/entropy/user_gauss_params/data/combine/" +
                   key+"_combined.csv", header=False, index=False)
    

combined_mxin = pd.concat(xi_list)
t1 = time.time()
print("Generate each individual combined file: ",t1-t0)

print("$$$$$$$$$$$$$$$$$$$$$")
print(total_rows)


t0 = time.time()
# 2. min and max for each file
dfTotalXI = combined_mxin.agg([min, max])
dfTotalXI.to_csv("/home/xphuang/entropy/user_gauss_params/data/combine/dfTotalXI.csv", header=False, index=False)

# 等权重的features可以加
total_sums = []
ui_row = []
user_vSum_dict  = {}
for key, value in dicts.items():
    user_vSum_dict[key]=0
    ui_row.append(0)




# 3. for each featureID (max, min)
user_vCount_dict = {}
featureID = 0
border_index_count = [0]*4096
for values in dfTotalXI.iteritems():  # for each feature
    print(featureID)
    v_feature_count = []
    xiLIST = (values[1].tolist()) # Thanks to Dennis 
    bMin = (xiLIST[0])
    bMax = (xiLIST[1])
    theRange = bMax - bMin

    # 3.1 for each user in the user_dict
    for key,value in dict(sorted(user_dict.items())).items():
        v_count=[0,0,0,0,0,0,0,0,0,0]
        feat_col = value.iloc[:,[featureID]]
        # print("lennn",len(feat_col.values.tolist()))
       
        # 3.1.1 for each value in this feature column
        for qq in feat_col.values.tolist():
            # print("qq", qq[0])
            index = int(10*(qq[0]-(1e-6)-bMin)/theRange)
            if index == 10:
                border_index_count += 1
                print("index",index)
                print("qq[0]-(1e-6)-bMin:",qq[0]-(1e-6)-bMin)
                print("qq[0]-bMin:",qq[0]-bMin)
                print("theRange: ",theRange)
                index=-1
            v_count[index]+=1
            user_vSum_dict.update({key:user_vSum_dict[key]+1})
        # user_vCount_dict[key+"_"+str(featureID)]=v_count
        v_feature_count.append(v_count)
    x = np.array(v_feature_count)
    x_normed = x / (x.max(axis=0) + 1e-6)
    summm = np.sum(x_normed, axis=1)
    np.savetxt("/home/xphuang/entropy/user_gauss_params/data/combine/sums/" + str(featureID)+"_sum.csv", summm, delimiter=",")
    np.savetxt("/home/xphuang/entropy/user_gauss_params/data/combine/sums/" + str(featureID)+"_x_normed.csv", x_normed, delimiter=",")
    np.savetxt("/home/xphuang/entropy/user_gauss_params/data/combine/sums/" + str(featureID)+"_x.csv", x, delimiter=",")
    
    for i in range(len(summm)):
        ui_row[i] +=  summm[i] 

    featureID+=1

result_list = []    
print(ui_row)
np.savetxt("/home/xphuang/entropy/user_gauss_params/data/combine/sums/ui_row.csv", ui_row, delimiter=",")
    
for item in ui_row:
    result_list.append(item/sum(ui_row))
np.savetxt("/home/xphuang/entropy/user_gauss_params/data/combine/sums/result_list.csv", result_list, delimiter=",")
    
print(result_list)

t1 = time.time()
print("Percentage Calculation Duration: ",t1-t0)
print(user_vSum_dict)
print("border_index_count: ", border_index_count)
# totalsum = 0
#  for key, value in user_vSum_dict.items():
#     totalsum.append()
    # for key, value in user_vCount_dict:
    #     if key.get

    # step = (float(bMax-bMin))/10
    # left_point = bMin
    # slice_counter = 0
  
    

# print(user_vSum_dict)
