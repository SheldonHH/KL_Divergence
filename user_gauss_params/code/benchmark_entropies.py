# features
#


#       0,1,2,3,4,5,6,7,8,9
#  u1   1
#  u2 

import numpy as np
import pandas as pd
import time
import os
import shutil
# import random
# dicts = {"user_1": [0, 30], "user_2": [3, 60], "user_3": [70, 140]}
# df = pd.read_csv(
#     "/home/xphuang/entropy/user_gauss_params/data/combine/space_small_q.csv", delimiter=" ")



userData_dict = {}


def benchmark(dicts, location_of_combined_file, combined_dir):
    # 0. Load combined_features.csv
    t0 = time.time()
    df = pd.read_csv(location_of_combined_file,  delimiter=" ")
    t1 = time.time()
    print("Step 0: loading combined.csv takes: ", t1-t0)
    # max, min for each user
    # xi_dict = {}

    # 1. Generate combined file for each user, read and write
    t0 = time.time()
    total_rows = 0  # to tally max, min for all users
    xi_list = [] 
    for key, value in dict(sorted(dicts.items())).items():
        dfRange = df.iloc[value[0]:value[1]] # integer-location based indexing for selection by position
        print(key,"'s row counts: ",len(dfRange))
        userData_dict[key] = dfRange
        # xi_dict[key] = (dfRange.agg([min, max]), len(dfRange))
        total_rows+=len(dfRange)
        xi_list.append(dfRange.agg([min, max]))
        dfRange.to_csv("/home/xphuang/entropy/user_gauss_params/data/combine/" +
                    key+"_combined.csv", header=False, index=False)
    t1 = time.time()
    print("Step 1. Generate each individual user file: ",t1-t0)
    # print("Check Total Row: ", total_rows)

    # 2.1 min and max for each file
    t0 = time.time()
    combined_mxin = pd.concat(xi_list)
    dfTotalXI = combined_mxin.agg([min, max])
    dfTotalXI.to_csv("/home/xphuang/entropy/user_gauss_params/data/combine/dfTotalXI.csv", header=False, index=False)
    t1 = time.time()
    print("Step 2.1 Generate global max, and min takes: ", t1-t0)

    # 2.2 Initialize ui_row_list
    t0 = time.time()
    ui_row_list = []      # 等权重的features可以加
    # user_vSum_dict  = {}
    for key, value in dicts.items():
        # user_vSum_dict[key]=0
        ui_row_list.append(0)
    t1 = time.time()
    print("Step 2.2 Initialize ui_row_list takes: ", t1-t0)


    
    # user_vCount_dict = {}
    # border_index_count = [0]*4096    # error checking
    # 3. foreach featureID (max, min)
    t0 = time.time()    
    featureID = 0
    for values in dfTotalXI.iteritems():  # for each feature
        print("featureID: ",featureID)
        v_feature_count = []
        xiLIST = (values[1].tolist()) # Thanks to Dennis 
        bMin = (xiLIST[0])
        bMax = (xiLIST[1])
        theRange = bMax - bMin
        # 3.1 for each user in the userData_dict
        # count items in each interval for each user
        for key,value in dict(sorted(userData_dict.items())).items():
            v_count=[0,0,0,0,0,0,0,0,0,0] # count items in each interval for each user
            feat_col = value.iloc[:,[featureID]]        
            # 3.1.1 for each value in THIS feature column of THIS user
            for qq in feat_col.values.tolist():
                # print("qq", qq[0])
                index = int(10*(qq[0]-(1e-6)-bMin)/theRange)
                # if index == 10:
                #     border_index_count += 1
                #     print("index",index)
                #     print("qq[0]-(1e-6)-bMin:",qq[0]-(1e-6)-bMin)
                #     print("qq[0]-bMin:",qq[0]-bMin)
                #     print("theRange: ",theRange)
                #     index=-1
                v_count[index]+=1
                # user_vSum_dict.update({key:user_vSum_dict[key]+1})
            # user_vCount_dict[key+"_"+str(featureID)]=v_count
            v_feature_count.append(v_count)
        x = np.array(v_feature_count)
        x_normed = x / (x.max(axis=0) + 1e-6)
        norm_summm = np.sum(x_normed, axis=1)
        # np.savetxt(combined_dir+"/sums/" + str(featureID)+"_sum.csv", norm_summm, delimiter=",")
        # np.savetxt(combined_dir+"/sums/" + str(featureID)+"_x_normed.csv", x_normed, delimiter=",")
        # np.savetxt(combined_dir+"/sums/" + str(featureID)+"_x.csv", x, delimiter=",")
        
        # keep tally for user [i] under each feature (outer loop)
        for i in range(len(norm_summm)):
            ui_row_list[i] +=  norm_summm[i] 
        featureID+=1
    t1 = time.time()
    print("3. Percentage Calculation Duration: ",t1-t0)


    bench_percent_list = []    
    print(ui_row_list)
    np.savetxt(combined_dir+"/results/ui_row_list.csv", ui_row_list, delimiter=",")
        
    for item in ui_row_list:
        bench_percent_list.append(item/sum(ui_row_list))
    np.savetxt(combined_dir+"/results/bench_percent_list.csv", bench_percent_list, delimiter=",")
    print(bench_percent_list)

    # print(user_vSum_dict)


def main():
    dicts = {"user_1": [1, 10000], "user_2": [10000, 20000], "user_3": [20000, 30000], "user_4": [30000,40000], "user_5": [40000,50000], "user_6": [50000,60000]}
    combined_file_name =  "user_2_comnbined.csv"
    combined_dir = "/home/xphuang/entropy/user_gauss_params/data/combine/"
    t0 = time.time()
    removeAllFiles(combined_dir+"sums/")
    removeAllFiles(combined_dir+"results/")
    t1 = time.time()
    print("Removed All Files sum Folders: ", t1-t0)
    benchmark(dicts, combined_dir+combined_file_name, combined_dir)

def removeAllFiles(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == "__main__":
    main()
