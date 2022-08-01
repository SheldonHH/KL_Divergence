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

    # user_1
    numpy_array = np.loadtxt(
        "/root/KL_Divergence/user_gauss_params/data/user_1.csv", delimiter=",")
    user_name = "user_2"

    true_arg_datapath = [
        "/root/KL_Divergence/user_gauss_params/data/"]
    raw_csv_argv = [true_arg_datapath[0]+user_name+".csv"]
    raw_csv_path1 = raw_csv_argv[0]

    # raw to image
    # for i in range(len(numpy_array)):
    #     raw_to_img([numpy_array[i]], user_name, str(i))
    # img_to_fea(numpy_array, true_arg_datapath, )
    img_to_fea_fast(numpy_array, true_arg_datapath,
                    user_name, len(numpy_array))

    t1 = time.time()
    print(t1-t0)
    ########################################################################

    #  image to features
    # for i in range(len(numpy_array)):
    #     # numpy_array[i]
    #     # if i <= 2:
    #     if os.path.exists(true_arg_datapath[0]+"features/"+user_name+"_features_"+str(i)+".csv") == False:
    #         single_file_feature = dynamic_gauss([numpy_array[i]], user_name, str(i))
    #         np.savetxt(true_arg_datapath[0]+user_name+"_features_"+str(i)+".csv", single_file_feature)
    #         nested_features.append(single_file_feature)
    #         print(i)
    # else:
    #     break

    # nested_features = []

    # true_arg_datapath = [
    #     "/root/KL_Divergence/user_gauss_params/data/"]
    # raw_csv_argv = [true_arg_datapath[0]+user_name+".csv"]
    # raw_csv_path1 = raw_csv_argv[0]

    # path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    # username = raw_csv_path1[raw_csv_path1.rindex('/')+1: raw_csv_path1.rindex('.')]
    # np.savetxt(user_name+'_joints.csv', nested_features)
    # print(len(nested_features))
    # for idx,col in enumerate(np.array(nested_features).T):
    #     print(col.tolist())
    #     # round_data_golang.round_data(raw_csv_argv,col.tolist())
    #     freq_to_gauss_golang.freq_to_gauss(raw_csv_argv, len(numpy_array), col, str(idx))
    # break

    # print(len(nested_features[0]))

    # pd.DataFrame(nested_features).T.to_csv(path+username+"_joints_"+".csv", header=False, index=False)

# 74.2619972229003


def raw_to_img(numpy_array, user_name, index_of_image):
    # print(raw_csv_argv)
    raw_csv_argv = [
        "/root/KL_Divergence/user_gauss_params/data/"+user_name+".csv"]
    raw_data_len = csv_to_jpeg.csv_to_jpeg(
        numpy_array, raw_csv_argv, index_of_image, user_name)
    # return extract_features(raw_csv_argv, index_of_image)
    # print(single_file_feature)

    # round_data_golang.round_data(raw_csv_argv)
    # countFreq_golang.count_freq(raw_csv_argv)
    # freq_to_gauss_golang.freq_to_gauss(raw_csv_argv, raw_data_len)


def img_to_fea(numpy_array, true_argv, user_name):
    new_fea_path = true_argv[0]+"features/"+user_name+"/"
    if os.path.isdir(new_fea_path) == False:
        os.mkdir(new_fea_path)  # make dir for that user
    nested_features = []
    psedo_csv_path_img = [
        "/root/KL_Divergence/user_gauss_params/data/image/"+user_name+"/"+user_name+".csv"]
    for i in range(len(numpy_array)):
        if os.path.exists(new_fea_path+user_name+"_features_"+str(i)+".csv") == False:
            single_file_feature = extract_features(psedo_csv_path_img,  str(i))
            np.savetxt(new_fea_path+user_name+"_features_" +
                       str(i)+".csv", single_file_feature)
            nested_features.append(single_file_feature)
            # print(i)


def img_to_fea_fast(numpy_array, true_argv, user_name, lens):
    true_datapath = "/root/KL_Divergence/user_gauss_params/data/"
    extract_features_fast(true_datapath, user_name, lens)

    # print(i)


if __name__ == "__main__":
    main()
