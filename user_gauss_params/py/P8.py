# features
#


#       0,1,2,3,4,5,6,7,8,9
#  u1   1
#  u2 

import numpy as np
import pandas as pd
import random
dicts = {"user_1": [0, 30], "user_2": [3, 60], "user_3": [70, 140]}
df = pd.read_csv(
    "/home/xphuang/entropy/user_gauss_params/data/combine/space_small_q.csv", delimiter=" ")


# dfRange = df.iloc[start:end]
# value:[]
user_dict = {}
xi_dict = {}
xi_list = []


total_rows = 0
for key, value in dicts.items():
    dfRange = df.iloc[value[0]:value[1]]
    print(len(dfRange))
    user_dict[key] = dfRange
    xi_dict[key] = (dfRange.agg([min, max]), len(dfRange))
    total_rows+=len(dfRange)
    
    xi_list.append(dfRange.agg([min, max]))

    dfRange.to_csv("/home/xphuang/KL_Divergence/user_gauss_params/data/combine/" +
                   key+"_combined.csv", header=False, index=False)
    
    # df.agg([min, max])

result = pd.concat(xi_list)


total_size = total_rows
print(total_size)
print("$$$$$$$$$$$$$$$$$$$$$")
print(total_rows)


this_fea_points_to_sample = total_size * 4096/100
dfTotalXI = result.agg([min, max])
dfTotalXI.to_csv("/home/xphuang/KL_Divergence/user_gauss_params/data/combine/dfTotalXI.csv", header=False, index=False)


#     max = max(Total_maxList)
#     min = min(Total_minList)
#     sample_range = max-min
#     step = sample_range/10
#     left_point = min
totalRange_List=[]

user_percent={} # for all features {user:[percent]}
# 1. create slices     # for each feature/col access as featureID_counter


# 等权重的features可以加
user_Fea_xis_dict = {} 
featureID_counter = 0
total_sums = []
ui_row = []
user_vSum_dict  = {}
for key, value in dicts.items():
    user_vSum_dict[key]=0
    ui_row.append(0)

user_vCount_dict = {}
featureID = 0
for values in dfTotalXI.iteritems():  # for each feature
    print(featureID_counter)
    xiLIST = (values[1].tolist()) # Thanks to Dennis 
    bMin = (xiLIST[0])
    bMax = (xiLIST[1])
    step = (bMax - bMin) / 10
    left = bMin
    
    v_feature_count = []
    # ready_vstack = 
    for key,value in sorted(user_dict.items()):
        print(key)
        v_count=[0,0,0,0,0,0,0,0,0,0]
        feat_col = value.iloc[:,[featureID_counter]]
        # print(feat_col.values.tolist()[0])

        for qq in feat_col.values.tolist():
            # print(qq[0])
            i = 0
            while i<=9:
                if qq[0] >= left and qq[0] <= step*i + left: 
                    v_count[i]+=1
                i+=1
        user_vSum_dict.update({key:user_vSum_dict[key]+1})
        user_vCount_dict[key+"_"+str(featureID)]=v_count
        v_feature_count.append(v_count)
        x = np.array(v_feature_count)
        x_normed = x / (x.max(axis=0) + 1e-6)
        # print(x_normed)
        
        # np.savetxt(str(featureID)+"x_normed.csv", x_normed, delimiter=",")
        summm = np.sum(x_normed, axis=1)
        np.savetxt(str(featureID)+"_sum.csv", summm, delimiter=",")
        print(summm)
        # for itemsum in summm:
        #     print(itemsum)
        
        for i in range(len(summm)):
            ui_row[i] +=  summm[i]
        # summm = np.sum(x_normed,axis=1).tolist()
        # np.vstack(sum)  
    featureID+=1
    featureID_counter += 1

result_list = []    
print(ui_row)
for item in ui_row:
    result_list.append(item/sum(ui_row))

print(result_list)
# totalsum = 0
#  for key, value in user_vSum_dict.items():
#     totalsum.append()
    # for key, value in user_vCount_dict:
    #     if key.get

    # step = (float(bMax-bMin))/10
    # left_point = bMin
    # slice_counter = 0
  
    

# print(user_percent)
# print(user_vSum_dict)
