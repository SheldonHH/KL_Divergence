import json
import random
import numpy as np
from datetime import datetime
import time
from functools import reduce
# generate random samples
def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)

def g_to_e(gauss_folder_ID, inputUsersLen):
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
    gauss_folder_ID = "one_gauss"
    for ifeaID in range(4096):
        print(ifeaID)
        Total_minList=[]
        Total_maxList=[]
        # calculate the bMin, bMax
        feaID = str(ifeaID)
        r_united_params_json = true_datapath + \
                "united_gauss/"+gauss_folder_ID+"/"+feaID+"/"+feaID+".json"
        f = open(r_united_params_json)
        data = json.load(f)
        # print(data)
        ui_row = []

        # Gauss Number check
        if (len(data.keys()) !=inputUsersLen):
            print("!!!!",data.keys())
            break
        
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


        left = bMin
        step = (bMax - bMin) / 10

    # print(data)

        v_feature_count = []

        for key,value in data.items():
            v_count=[0,0,0,0,0,0,0,0,0,0]
            d_mins = value["min"]
            d_maxs = value["max"]
            d_weights = value["weights"]
            d_uf_size = int(value["raw_data_size"])
            all_sam_points = []
            for i in range(len(d_maxs)):
                sam_point1 = [random.uniform(d_mins[i], d_maxs[i]) for x in range(int(d_uf_size*d_weights[i])*100)]
                all_sam_points+=sam_point1
            # print("@!#$@#$#@$@#$@#$",len(all_sam_points))
            # break
            for qq in all_sam_points:
                i = 0
                while i<=9:
                    if qq >= left and qq <= step*i + left: 
                        v_count[i]+=1
                    i+=1
            v_feature_count.append(v_count)
            # print(v_count)
            x = np.array(v_feature_count)
            np.savetxt("x.csv", x, delimiter=",")
            x_normed = x / (x.max(axis=0) + 1e-6)
            summm = np.sum(x_normed, axis=1)
            np.savetxt("x_normed.csv", x_normed, delimiter=",")
            # print(summm)
            for i in range(len(summm)):
                ui_row[i] += summm[i]
        
        print(v_feature_count)
    print(ui_row)
    with open(true_datapath+gauss_folder_ID+"sum"".json", "w") as outfile:
        json.dump(ui_row, outfile)
    result_list = []    
    print(ui_row)
    for item in ui_row:
        result_list.append(item/sum(ui_row))
    print(result_list)
    str_date_time = datetime.fromtimestamp(time.time()).strftime("%m%d, %H:%M:%S")
    with open(true_datapath+gauss_folder_ID+"_gauss_percentage"".json", "w") as outfile:
        json.dump(result_list, outfile)
