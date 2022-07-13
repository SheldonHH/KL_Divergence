import pandas as pd
import random
dicts = {"user_1": [0, 30], "user_2": [3, 60], "user_3": [70, 140]}
df = pd.read_csv(
    "/home/xphuang/entropy/user_gauss_params/data/combine/space_small_q.csv", delimiter=" ")


# dfRange = df.iloc[start:end]
# value:[]
xi_dict = {}
xi_list = []
total_rows = 0
for key, value in dicts.items():
    dfRange = df.iloc[value[0]:value[1]]
    print(len(dfRange))
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
for values in dfTotalXI.iteritems():
    print(featureID_counter)
    xiLIST = (values[1].tolist()) # Thanks to Dennis 
    bMin = (xiLIST[0])
    bMax = (xiLIST[1])

    step = (float(bMax-bMin))/10
    left_point = bMin
    slice_counter = 0
    while left_point <= bMax-step:
        right_point = left_point+step
         # total number
        # print(slice_counter)
        for i in range(int(this_fea_points_to_sample/10)):
            sam_point = random.uniform(left_point, right_point)
            rangeList = []
            # for each user
            for key, value in xi_dict.items(): # for each user
                # print(xi_dict[key][0].iloc[featureID_counter])
                # print(type(xi_dict[key][0]))
                # print(featureID_counter)
                # print(xi_dict[key][0].columns[featureID_counter])
                subXILIST = xi_dict[key][0].iloc[:,[featureID_counter]].values.tolist()
                # print(subXILIST[0])
                # print(subXILIST[1])
                minn = subXILIST[0][0]
                maxx = subXILIST[1][0]
                # print(type(minn))
                # minn = xi_dict[0]
                # maxx = xi_dict[key][1].columns[featureID_counter]
                if sam_point >= minn and sam_point <= maxx:
                    if key in user_Fea_xis_dict:
                      newValue = user_Fea_xis_dict[key]+1
                      user_Fea_xis_dict.update({key: newValue})
                    else:
                      user_Fea_xis_dict[key]=1
                       
        left_point=right_point
        slice_counter+=1
        


    # for key, value in user_Fea_xis_dict.items():
    #     user_percent[key] = user_Fea_xis_dict[key]/this_fea_points_to_sample
    
    # user_Fea_xis_dict[]
            # print(eat)
    featureID_counter += 1

print(user_percent)


    
        # for each user
        # featureID_counter = 0
        # for subva in xi_dict[key][0].iteritems():
            # print(type(subva)) # tuple
            # print(subva[0])
            # featureID_counter+=1
        # print(featureID_counter)
    
    # xi_dict[key]
    # print("min:",values[0])
    # print("max",values[1])
    # T_range = values[1] - values[0]
    # step = T_range/10
    # left_point = values[0]
    # right_point = values[1]
    # num_eachrange = int(Total_rawDataSize/10)
    # right_point = 0
    # while left_point < max-step:
    #     right_point += left_point+step
    #     sam_point = random.uniform(left_point , right_point)
    #     rangeList = []
    #   for i in range(num_eachrange):
    #         for key, value in user_Fea_xis_dict.items():
    #             vList = tuple(value)
    #             if vList[0] < sam_point and sam_point > vList[1]:
    #                 user_Fea_xis_dict.update({key:tuple([vList[0], vList[1], vList[2], 1+vList[3]])})
        
    #     left_point=right_point
    #     totalRange_List.append(rangeList)       

# max, min, 
# for df in xi_dict:
#     for name, values in df.iteritems():
#         print('{name}: {value}'.format(name=name, value=values))



# for the column:
#     max = max(Total_maxList)
#     min = min(Total_minList)
#     sample_range = max-min
#     step = sample_range/10
#     left_point = min
#     num_eachrange = int(Total_rawDataSize/10)
#     right_point = 0
#     while left_point < max-step:
#     right_point += left_point+step
#     rangeList = []
#     for i in range(num_eachrange):
#         sam_point = random.uniform(left_point , right_point)
#         rangeList.append(sam_point)
#         for key, value in user_Fea_xis_dict.items():
#             vList = tuple(value)
#             if vList[0] < sam_point and sam_point > vList[1]:
#             user_Fea_xis_dict.update({key:tuple([vList[0], vList[1], vList[2], 1+vList[3]])})