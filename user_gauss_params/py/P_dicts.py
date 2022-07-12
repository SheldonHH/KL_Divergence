import pandas as pd

dicts = {"user_1": [1, 3], "user_2": [3, 6], "user_3": [7, 9]}
df = pd.read_csv(
    "/root/KL_Divergence/user_gauss_params/data/combine/all_combined.csv", delimiter=" ")


# dfRange = df.iloc[start:end]

xi_dict = {}
xi_list = []
for key, value in dicts.items():
    dfRange = df.iloc[value[0]:value[1]]
    print(len(dfRange))
    xi_dict[key] = (dfRange.agg([min, max]), len(dfRange))
    
    xi_list.append(dfRange.agg([min, max]))
    # print(dfRange.agg([min, max]))
    # print("individual size",len(dfRange))

    dfRange.to_csv("/root/KL_Divergence/user_gauss_params/data/combine/" +
                   key+"_combined.csv", header=False, index=False)
    # df.agg([min, max])

result = pd.concat(xi_list)
# print("total size",len(result))
# print(result.agg([min, max]))
total_size = len(xi_list)
Total_rawDataSize = total_size * 4096
dfTotalXI = result.agg([min, max])
dfTotalXI.to_csv("/root/KL_Divergence/user_gauss_params/data/combine/dfTotalXI.csv", header=False, index=False)

totalRange_List
# 1. create slices
for name, values in dfTotalXI.iteritems():
    print("min:",values[0])
    print("max",values[1])
    T_range = values[1] - values[0]
    step = T_range/10
    left_point = values[0]
    right_point = values[1]
    num_eachrange = int(Total_rawDataSize/10)
    right_point = 0
    while left_point < max-step:
        right_point += left_point+step
        sam_point = random.uniform(left_point , right_point)
        rangeList = []
      for i in range(num_eachrange):
            for key, value in user_Fea_xis_dict.items():
                vList = tuple(value)
                if vList[0] < sam_point and sam_point > vList[1]:
                    user_Fea_xis_dict.update({key:tuple([vList[0], vList[1], vList[2], 1+vList[3]])})
        
        left_point=right_point
        totalRange_List.append(rangeList)       

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