import json
import random
import numpy as np
from functools import reduce
# generate random samples
def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)

    
true_datapath = "/home/xphuang/entropy/user_gauss_params/data/"
# for ifeaID in range(4096):
#       print(ifeaID)
#       feaID=str(ifeaID)
#       r_united_params_json = true_datapath + \
#           "united_gauss/"+feaID+"/"+feaID+".json"
#       w_consolidated_percent_json = true_datapath + \
#           "entropy/entropysum_percent_"+feaID+".json"
#       f = open(r_united_params_json)
#       data = json.load(f)

#       Total_maxList=[]
#       Total_minList=[]
#       Total_rawDataSize = int(4096)


Total_minList=[]
Total_maxList=[]
# calculate the bMin, bMax
feaID = "1"
r_united_params_json = true_datapath + \
          "united_gauss/"+feaID+"/"+feaID+".json"
f = open(r_united_params_json)
data = json.load(f)
ui_row = []
for user_str in data.keys():
    ui_row.append(0)
    users_individual_gauss_entropy = []
    d_mins = data[user_str]["min"]
    d_maxs = data[user_str]["max"]
    d_uf_size = data[user_str]["raw_data_size"]
    Total_minList += d_mins
    Total_maxList += d_maxs
    # xiLIST = (values[1].tolist()) # Thanks to Dennis 
bMax = max(Total_maxList)
bMin = max(Total_minList)


left = bMin
step = (bMax - bMin) / 10
user_Fea_g_dict = {}



v_feature_count = []
for user_str in data.keys():
    v_count=[0,0,0,0,0,0,0,0,0,0]
    users_individual_gauss_entropy = []
    no_gauss = len(data[user_str]["min"])
    d_mins = data[user_str]["min"]
    d_maxs = data[user_str]["max"]
    d_weights = data[user_str]["weights"]
    d_uf_size = int(data[user_str]["raw_data_size"])*1000
    all_sam_points = []
    for i in range(len(d_weights)):
        sam_point1 = [random.uniform(d_mins[i], d_maxs[i]) for x in range(int(d_uf_size*d_weights[i]))]
        all_sam_points+=sam_point1
    for qq in all_sam_points:
        i = 0
        while i<=9:
            if qq >= left and qq <= step*i + left: 
                v_count[i]+=1
            i+=1
    v_feature_count.append(v_count)
    x = np.array(v_feature_count)
    x_normed = x / (x.max(axis=0) + 1e-6)
    summm = np.sum(x_normed, axis=1)
    np.savetxt(str(featureID)+"_sum.csv", summm, delimiter=",")
    print(summm)
    for i in range(len(summm)):
        ui_row[i] +=  summm[i]
    
    
print(ui_row)
    