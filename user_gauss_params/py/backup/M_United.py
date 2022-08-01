import json
import os
import sys
import pandas as pd
from functools import reduce

def write_dict_to_json(dict, json_to_write):
    df_params = pd.DataFrame.from_dict(dict)
    result = df_params.to_json(orient="columns")
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))

def json_under_this_dir(dir_in_str):
    directory = os.fsencode(dir_in_str)
    usergauss_list = []
    files_underfeaID = 0
    for file in os.listdir(directory):
        print(files_underfeaID)
        files_underfeaID+=1
        filename = os.fsdecode(file)
        # print(filename[filename.rfind("_")+1:filename.rfind(".")])
        if filename.endswith(".json"):
            usergauss_list.append(filename) 
            continue
        else:
            continue
    # print("usergauss_list",usergauss_list)
    return usergauss_list

def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)

def server_consolidate(subfolders, target_outerfolder):
    # print("required_userlist", required_userlist)
    # args = subfolders
    # fea_dirs = args[0]
    # print("subfolders",subfolders)
    feaCounter = 0
    for subf in subfolders:
        consolidated_params = {}
        print(feaCounter)
        feaCounter+=1
        fea_dirs = subf
        # print("fea_dirs",fea_dirs)
        print("subf",subf)
        print("featureID:",subf[subf.rfind("/")+1:len(subf)])
        featureID = subf[subf.rfind("/")+1:len(subf)]
        users_list = json_under_this_dir(fea_dirs)
        for user_gauss_file in users_list:
            # print(user_gauss_file)
            # if user_gauss_file[0:findNth(user_gauss_file, "_",2)] in required_userlist:
            #     print("sdfds",user_gauss_file[0:findNth(user_gauss_file, "_",2)])
                # if 'time' in required_userlist :
                # username = user_gauss_file[0: user_gauss_file.rindex('.')]
            with open(fea_dirs+"/"+user_gauss_file) as json_file:
                data_dict = json.load(json_file)
                pk = list(data_dict.keys())[0]
                print("pk",pk[pk.rfind("_")+1:len(pk)])
                consolidated_params[pk] = data_dict[pk]
        output_specified_dir = target_outerfolder+str(featureID)+"/"
        if os.path.isdir(output_specified_dir) == False:
            os.mkdir(output_specified_dir)
        w_consolidated_gauss_params_json = output_specified_dir+str(featureID)+".json"
        # print(w_consolidated_gauss_params_json)
        write_dict_to_json(consolidated_params, w_consolidated_gauss_params_json)




def unit_gauss(users_list, gauss_folder_ID):
    individual_gauss = ["/home/xphuang/entropy/user_gauss_params/data/users_individual_gauss/"+gauss_folder_ID+"/"] # location where stores individual gauss
    directory = individual_gauss[0]
    subfolders = [x[0] for x in os.walk(directory)]
    print(subfolders)
    print('len',len(subfolders))
    target_outerfolder = "/home/xphuang/entropy/user_gauss_params/data/united_gauss/"+gauss_folder_ID+"/"
    if os.path.isdir(target_outerfolder) == False:
        os.mkdir(target_outerfolder)
    # for featureID in range(4096):
    server_consolidate(subfolders, target_outerfolder)

# def main():
#     unit_gauss=
  # calculate_entropy_golang.calculate_entropy(individual_gauss)


# if __name__ == "__main__":
#     main()