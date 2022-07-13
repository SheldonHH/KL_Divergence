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

user_vSum_dict  = {}
for key, value in dicts.items():
    user_vSum_dict[key]=0

user_vCount_dict = {}
featureID = 0
for values in dfTotalXI.iteritems():  # for each feature
    print(featureID_counter)
    xiLIST = (values[1].tolist()) # Thanks to Dennis 
    bMin = (xiLIST[0])
    bMax = (xiLIST[1])
    step = (bMax - bMin) / 10
    left = bMin
    
    for key,value in user_dict.items():
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
    featureID+=1


totalsum = 0
 for key, value in user_vSum_dict.items():
    totalsum.append()
    # for key, value in user_vCount_dict:
    #     if key.get

    # step = (float(bMax-bMin))/10
    # left_point = bMin
    # slice_counter = 0
  
    featureID_counter += 1

print(user_percent)
print(user_vSum_dict)
