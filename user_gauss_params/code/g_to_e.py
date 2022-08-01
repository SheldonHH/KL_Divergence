import json
import random
import numpy as np
from datetime import datetime
import time
import os
from functools import reduce
# generate random samples
def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)

def g_to_e(gauss_folder_ID, inputUsersLen, samplePercent):
    true_datapath = "/home/xphuang/entropy/user_gauss_params/data/"
    gauss_folder_ID = "one_gauss"
    for ifeaID in range(4096):
        print(ifeaID)
        Total_minList=[]
        Total_maxList=[]
        
        # 1. calculate bMin, bMax
        feaID = str(ifeaID)
        r_united_params_json = true_datapath + \
                "united_gauss/"+gauss_folder_ID+"/"+feaID+"/"+feaID+".json"
        f = open(r_united_params_json)
        data = json.load(f)
        ui_row = []

        # 2. Gauss Number check
        if (len(data.keys()) != inputUsersLen):
            print("!!!!",data.keys())
            break
        
        # 3. obtain max, min, order doesn't matter
        for key,value in data.items():
            ui_row.append(0)
            d_mins = value["min"]
            d_maxs = value["max"]
            d_uf_size = value["raw_data_size"]
            Total_minList += d_mins
            Total_maxList += d_maxs
            # xiLIST = (values[1].tolist()) # Thanks to Dennis 
        
        # bMax, bMin for the list
        bMax = max(Total_maxList)
        bMin = min(Total_minList)
        theRange = bMax - bMin

        v_feature_count = []

        for ukey,value in data.items():
            v_count=[0,0,0,0,0,0,0,0,0,0]
            d_mins = value["min"]
            d_maxs = value["max"]
            d_weights = value["weights"]
            d_uf_size = int(value["raw_data_size"])
            all_sam_points = []
            for i in range(len(d_maxs)):
                sam_point1 = [random.uniform(d_mins[i], d_maxs[i]) for x in range(int(d_uf_size*d_weights[i]*(samplePercent/100)))]
                all_sam_points+=sam_point1
            for pointNum in all_sam_points:
                index = int(10*(pointNum-bMin)/theRange)
                v_count[index]+=1
            v_feature_count.append(v_count)
            # print(v_count)
            x = np.array(v_feature_count)
            x_normed = x / (x.max(axis=0) + 1e-6)
            summm = np.sum(x_normed, axis=1)
            # np.savetxt(true_datapath + \
            #     "united_gauss/"+gauss_folder_ID+"/"+feaID+"/"+ukey+"x_"+gauss_folder_ID+".csv", x, delimiter=",")
            # np.savetxt(true_datapath + \
            #     "united_gauss/"+gauss_folder_ID+"/"+feaID+"/"+ukey+"x_norm_"+gauss_folder_ID+".csv", x_normed, delimiter=",")
            # with open(true_datapath+ \
            #     "united_gauss/"+gauss_folder_ID+"/"+feaID+"/"+ukey+"_sum.csv", "w") as outfile:
            #     json.dump(ui_row, outfile)
            for i in range(len(summm)):
                ui_row[i] += summm[i]

    gauss_result_list = []    
    print(ui_row)
    for item in ui_row:
        gauss_result_list.append(item/sum(ui_row))
    print(gauss_result_list)
    benchmark_subFolder = true_datapath+"benchmark/"
    if os.path.isdir(benchmark_subFolder) == False:
        os.makedirs(benchmark_subFolder, exist_ok=True)
    str_date_time = datetime.fromtimestamp(time.time()).strftime("%m%d, %H:%M:%S")
    with open(benchmark_subFolder+gauss_folder_ID+"_ui_row"+str_date_time+".json", "w") as outfile:
        json.dump(ui_row, outfile)
    with open(benchmark_subFolder+gauss_folder_ID+"_gauss_percentage"+str_date_time+".json", "w") as outfile:
        json.dump(gauss_result_list, outfile)
