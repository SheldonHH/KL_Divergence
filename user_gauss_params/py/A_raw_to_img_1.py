from tally import csv_to_jpeg
from py_torch.FeatureExtractor import extract_features
from py_torch.FeatureExtractor import extract_features_fast
from tally import round_data_golang
from tally import countFreq_golang
from tally import freq_to_gauss_golang
import numpy as np
import os.path
import time
import pandas as pd
# from tally import features_extractor


def main():
    t0 = time.time()
    # Two Inputs
    # numpy_array = np.loadtxt(
    #     "/root/KL_Divergence/user_gauss_params/data/user_4.csv", delimiter=",")
    # user_name = "user_4"

    # user_2
    user_name = "user_2"
    numpy_array = np.loadtxt(
        "/root/KL_Divergence/user_gauss_params/data/"+user_name+".csv", delimiter=",")

    true_datapath = "/root/KL_Divergence/user_gauss_params/data/"

    # raw to image
    for i in range(len(numpy_array)):
        print()
        if i != 0:
            print(i)
            raw_to_img([numpy_array[i]], true_datapath, user_name, str(i))
        else: 
            print(numpy_array[i])
    # img_to_fea(numpy_array, true_arg_datapath, )
    # img_to_fea_fast(numpy_array, true_arg_datapath, user_name, len(numpy_array))

    t1 = time.time()
    print(t1-t0)
    ########################################################################


def raw_to_img(numpy_array, true_datapath, user_name, index_of_image):
    # print(raw_csv_argv)
    raw_csv_argv = ["/root/KL_Divergence/user_gauss_params/data/"+user_name+".csv"]
    new_img_path = true_datapath+"image/"+user_name+"/"
    if os.path.isdir(new_img_path) == False:
        os.mkdir(new_img_path)
    raw_data_len = csv_to_jpeg.csv_to_jpeg(numpy_array, raw_csv_argv, index_of_image, user_name)



# def img_to_fea(numpy_array, true_argv, user_name):
#     new_fea_path = true_argv[0]+"features/"+user_name+"/"
#     if os.path.isdir(new_fea_path) == False:
#         os.mkdir(new_fea_path) # make dir for that user
#     nested_features = []
#     psedo_csv_path_img = ["/root/KL_Divergence/user_gauss_params/data/image/"+user_name+"/"+user_name+".csv"]
#     for i in range(len(numpy_array)):
#         if os.path.exists(new_fea_path+user_name+"_features_"+str(i)+".csv") == False:
#             single_file_feature = extract_features(psedo_csv_path_img,  str(i))
#             np.savetxt(new_fea_path+user_name+"_features_"+str(i)+".csv", single_file_feature)
#             nested_features.append(single_file_feature)
            # print(i)


# def img_to_fea_fast(numpy_array, true_datapath, user_name, lens):
#     true_datapath = "/root/KL_Divergence/user_gauss_params/data/"
#     extract_features_fast(true_datapath, user_name, lens)
 
            # print(i)

if __name__ == "__main__":
    main()
