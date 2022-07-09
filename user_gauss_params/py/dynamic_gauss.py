from tally import csv_to_jpeg
from py_torch.FeatureExtractor import extract_features
from tally import round_data_golang
from tally import countFreq_golang
from tally import freq_to_gauss_golang
import numpy as np
import os.path

import pandas as pd
# from tally import features_extractor


def main():
    # Two Inputs
    numpy_array = np.loadtxt(
        "/root/KL_Divergence/user_gauss_params/data/user_4.csv", delimiter=",")
    user_name = "user_4"
    # for i in range(len(numpy_array)):
    #     dynamic_gauss([numpy_array[i]], user_name, str(i))


    real_raw_csv_argv = [
        "/root/KL_Divergence/user_gauss_params/data/"]
    raw_csv_argv = [real_raw_csv_argv[0]+user_name+".csv"]
    raw_csv_path1 = raw_csv_argv[0]

    ########################################################################
    
    nested_features = []
    for i in range(len(numpy_array)):
        # numpy_array[i]
        # if i <= 2:
        if os.path.exists(real_raw_csv_argv[0]+"features/"+user_name+"_features_"+str(i)+".csv") == False:
            single_file_feature = dynamic_gauss([numpy_array[i]], user_name, str(i))
            np.savetxt(real_raw_csv_argv[0]+user_name+"_features_"+str(i)+".csv", single_file_feature)
            nested_features.append(single_file_feature)
            print(i)
        # else:
        #     break
    


    real_raw_csv_argv = [
        "/root/KL_Divergence/user_gauss_params/data/"]
    raw_csv_argv = [real_raw_csv_argv[0]+user_name+".csv"]
    raw_csv_path1 = raw_csv_argv[0]

    path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    username = raw_csv_path1[raw_csv_path1.rindex('/')+1: raw_csv_path1.rindex('.')]
    np.savetxt(user_name+'_joints.csv', nested_features)
    print(len(nested_features))
    for idx,col in enumerate(np.array(nested_features).T):
        print(col.tolist())
        # round_data_golang.round_data(raw_csv_argv,col.tolist())
        freq_to_gauss_golang.freq_to_gauss(raw_csv_argv, len(numpy_array), col, str(idx))
        # break
        
    
    # print(len(nested_features[0]))

    # pd.DataFrame(nested_features).T.to_csv(path+username+"_joints_"+".csv", header=False, index=False)


def dynamic_gauss(numpy_array, user_name, index_of_image):
    # print(raw_csv_argv)
    # raw_data_len = csv_to_jpeg.csv_to_jpeg(numpy_array, raw_csv_argv,index_of_image)
    raw_csv_argv = ["/root/KL_Divergence/user_gauss_params/data/"+user_name+".csv"]
    return extract_features(raw_csv_argv, index_of_image)
    # print(single_file_feature)
   
    # round_data_golang.round_data(raw_csv_argv)
    # countFreq_golang.count_freq(raw_csv_argv)
    # freq_to_gauss_golang.freq_to_gauss(raw_csv_argv, raw_data_len)


if __name__ == "__main__":
    main()
