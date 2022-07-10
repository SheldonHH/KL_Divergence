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

def user_list_from_dir(dir_in_str):
    directory = os.fsencode(dir_in_str)
    usergauss_list = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            usergauss_list.append(filename) 
            continue
        else:
            continue
    print("usergauss_list",usergauss_list)
    return usergauss_list

def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)

def server_consolidate(individual_gauss, required_userlist):
    print("required_userlist", required_userlist)
    args = individual_gauss
    gauss_users_dir = args[0]
    consolidated_params = {}
    print("gauss_users_dir",gauss_users_dir)
    users_list = user_list_from_dir(gauss_users_dir)
    print("users_list",users_list)
#     for user_gauss_file in users_list:
#         if user_gauss_file[0:findNth(user_gauss_file, "_",2)] in required_userlist:
#             # if 'time' in required_userlist :
#             # username = user_gauss_file[0: user_gauss_file.rindex('.')]
#             with open(gauss_users_dir+"/"+user_gauss_file) as json_file:
#                 data_dict = json.load(json_file)
#                 pk = list(data_dict.keys())[0]
#                 consolidated_params[pk] = data_dict[pk]
#     w_consolidated_gauss_params_json = gauss_users_dir + "/consolidated/consolidated_gauss_params.json"
#     write_dict_to_json(consolidated_params, w_consolidated_gauss_params_json)


# def write_profit_weight_to_json(list, json_to_write):
#     df_params = pd.Series(list).to_frame("profit_weight")
#     print(df_params)
#     result = df_params.to_json(orient="index")
#     parsed = json.loads(result)
#     with open(json_to_write, 'w') as convert_file:
#         convert_file.write(json.dumps(parsed))

