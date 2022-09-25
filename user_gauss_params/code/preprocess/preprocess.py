from csv_to_img import csv_to_jpeg
from py_torch.FeatureExtractor import step_2_extract_features_fast
import numpy as np
import os.path
import time
import glob
import os
import csv
import time
import natsort

# from tally import features_extractor
 


def step_1_raw_to_img(rawdata_arr, true_datapath, rawdata_tag, index_of_image):
    raw_csv_argv = [true_datapath+rawdata_tag+".csv"]
    new_img_path = true_datapath+"image/"+rawdata_tag+"/"
    if os.path.isdir(new_img_path) == False:
        os.mkdir(new_img_path)
    # generate .jpeg from raw .csv
    csv_to_jpeg.csv_to_jpeg(rawdata_arr, raw_csv_argv, index_of_image, rawdata_tag)


# from data row to feature_based csv file
def step_3_transpose_csv(true_datapath):
    input_file_list = glob.glob(true_datapath + "features/preprocess/*.csv")
    counter = 0
    for inputfile in input_file_list:
        outputfile = true_datapath+"transposed_features/preprocess/transposed_"+str(counter)+".csv"
        a = zip(*csv.reader(open(inputfile, "rt")))
        csv.writer(open(outputfile, "wt")).writerows(a)
        counter += 1

def step_4_combine_feature_files(transposed_inputs_dir, target_fullPath):
    extension = 'csv'
    transposed_inputs_list = glob.glob(transposed_inputs_dir+'*.{}'.format(extension))
    sorted_files = natsort.natsorted(transposed_inputs_list)
    all_filenames = [i for i in sorted_files]
    print(len(all_filenames))
    counterrr = 0
    sorted_filenames = natsort.natsorted(all_filenames)
    with open(target_fullPath, "w") as f:
        for file in sorted_filenames:
            print(counterrr)
            counterrr+=1
            with open(file) as fff:
                f.write(fff.read())
                
                
                
def main():
    rawdata_tag = "raw_dataset"
    raw_datapath = "/home/code/user_gauss_params/data/"+rawdata_tag+".csv"

    t0 = time.time()
    rawdata_arr = np.loadtxt(raw_datapath, delimiter=",")
    true_datapath = "/home/code/user_gauss_params/data/"
    # raw to image
    for i in range(len(rawdata_arr)):
        print()
        if i != 0:
            print(i)
            step_1_raw_to_img([rawdata_arr[i]], true_datapath, rawdata_tag, str(i))
        else: 
            print(rawdata_arr[i])
    t1 = time.time()
    print("Step 1: Time takes for raw_dataset to image: ", t1-t0)
    
    true_datapath = "/home/code/user_gauss_params/data/"    
    
    t0 = time.time()
    step_2_extract_features_fast(true_datapath, "preprocess", len(rawdata_arr))
    t1 = time.time()
    print("Step 2: Time takes for generating feature file for each user: ", t1-t0)

    t0 = time.time()
    step_3_transpose_csv(true_datapath, "")
    t1 = time.time()
    print("Step 3: Time takes for transposing CSV file: ", t1-t0)
    
    transposed_inputs_dir = "/home/code/user_gauss_params/data/transposed_features/preprocess/"
    target_fullPath = "/home/code/user_gauss_params/data/combine/preprocessed_dataset.csv"
    t0 = time.time()
    step_4_combine_feature_files(transposed_inputs_dir,target_fullPath)
    t1 = time.time()
    print("Step 4: Time takes to combine individual feature file: ", t1-t0)





if __name__ == "__main__":
    main()
