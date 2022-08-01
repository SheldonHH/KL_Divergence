import json
import os
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
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            usergauss_list.append(filename) 
            continue
        else:
            continue
    return usergauss_list

def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)

def server_consolidate(selected_users_set, gFea_subFolders, target_outerfolder):
    # userCounter = 0
    # for each user in the feature folder
    for idx,subf in enumerate(gFea_subFolders):
        consolidated_params = {}
        # print("userCounter for this feature", userCounter)
        the_fea_dir = subf
        # print("subf",subf)
        print("featureID:",subf[subf.rfind("/")+1:len(subf)])
        featureID = subf[subf.rfind("/")+1:len(subf)]
        users_list = json_under_this_dir(the_fea_dir)
        for user_gauss_file in users_list:
            username = user_gauss_file[0:findNth(user_gauss_file, "_", 2)]
            # username in selected_users_set lookup/insert/delete in O(1) for set python
            if username in selected_users_set:
                # userCounter+=1
                with open(the_fea_dir+"/"+user_gauss_file) as json_file:
                    data_dict = json.load(json_file)
                    pk = list(data_dict.keys())[0]
                    # print("pk",pk[pk.rfind("_")+1:len(pk)])
                    consolidated_params[pk] = data_dict[pk]
        output_specified_dir = target_outerfolder+str(featureID)+"/"
        if os.path.isdir(output_specified_dir) == False:
            os.mkdir(output_specified_dir)
        
        # Consolidated Gauss Result for the featureID filtered by selected user set
        w_consolidated_gauss_params_json = output_specified_dir+str(featureID)+".json"
        write_dict_to_json(consolidated_params, w_consolidated_gauss_params_json)




def unite_gauss(selected_users_set, gauss_folder_ID):
    individual_gauss = ["/home/xphuang/entropy/user_gauss_params/data/users_individual_gauss/"+gauss_folder_ID+"/"] # location where stores individual gauss
    directory = individual_gauss[0]
    print("selected_users_set", selected_users_set)
    # every featureID under one_gauss folder exclude the folder itself
    unsorted_subF = [x[0] for x in os.walk(directory) if x[0] != individual_gauss[0]] 
    gFea_subFolders = sorted(unsorted_subF, key=lambda x: int(x[x.rfind("/")+1:len(x)]) if x != "" else x)
    # for x in gFea_subFolders:
    #     print(int(x[x.rfind("/")+1:len(x)])) 
    print('len',len(gFea_subFolders))
    target_outerfolder = "/home/xphuang/entropy/user_gauss_params/data/united_gauss/"+gauss_folder_ID+"/"
    if os.path.isdir(target_outerfolder) == False:
        os.mkdir(target_outerfolder)
    server_consolidate(selected_users_set, gFea_subFolders, target_outerfolder)

