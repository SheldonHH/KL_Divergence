from tally import calculate_entropy_golang 
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

def user_list_from_dir(dir_in_str, featureID):
    directory = os.fsencode(dir_in_str)
    usergauss_list = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # print(filename[filename.rfind("_")+1:filename.rfind(".")])
        if filename.endswith(".json") and (filename[filename.rfind("_")+1:filename.rfind(".")] == featureID):
            usergauss_list.append(filename) 
            continue
        else:
            continue
    print("usergauss_list",usergauss_list)
    return usergauss_list

def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)

def server_consolidate(subfolders, required_userlist, featureID, target_outerfolder):
    print("required_userlist", required_userlist)
    # args = subfolders
    # gauss_users_dir = args[0]
    consolidated_params = {}
    for subf in subfolders:
        gauss_users_dir = subf
        print("gauss_users_dir",gauss_users_dir)
        print("subf",subf)
        users_list = user_list_from_dir(gauss_users_dir, featureID)
        # print("users_list",users_list)
        for user_gauss_file in users_list:
            if user_gauss_file[0:findNth(user_gauss_file, "_",2)] in required_userlist:
                print("sdfds",user_gauss_file[0:findNth(user_gauss_file, "_",2)])
                # if 'time' in required_userlist :
                # username = user_gauss_file[0: user_gauss_file.rindex('.')]
                with open(gauss_users_dir+"/"+user_gauss_file) as json_file:
                    data_dict = json.load(json_file)
                    pk = list(data_dict.keys())[0]
                    consolidated_params[pk] = data_dict[pk]
        output_specified_dir = target_outerfolder+featureID+"/"
        if os.path.isdir(output_specified_dir) == False:
            os.mkdir(output_specified_dir)
        w_consolidated_gauss_params_json = output_specified_dir+featureID+".json"
        write_dict_to_json(consolidated_params, w_consolidated_gauss_params_json)



def main():
  individual_gauss = ["/root/KL_Divergence/user_gauss_params/data/users_individual_gauss"] # location where stores individual gauss
  directory = individual_gauss[0]
  users_list = ["user_1", "user_4"]
  subfolders = [x[0] for x in os.walk(directory)]
  print(subfolders)
  print(len(subfolders))
  feature_to_united = ["0"]
  target_outerfolder = "/root/KL_Divergence/user_gauss_params/data/united_gauss/"
  for featureID in feature_to_united:
    server_consolidate(subfolders, users_list, featureID, target_outerfolder)
  # calculate_entropy_golang.calculate_entropy(individual_gauss)


if __name__ == "__main__":
    main()