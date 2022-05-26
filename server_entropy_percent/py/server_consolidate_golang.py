import json
import os
import sys
import pandas as pd


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
    return usergauss_list

def main():
    args = sys.argv[1:]
    gauss_users_dir = args[0]
    consolidated_params = {}
    print("gauss_users_dir",gauss_users_dir)
    users_list = user_list_from_dir(gauss_users_dir)
    print("users_list",users_list)
    for user_gauss_file in users_list:
        with open(gauss_users_dir+"/"+user_gauss_file) as json_file:
            data_dict = json.load(json_file)
            print(data_dict)
            print("user_gauss_file[0:5]",user_gauss_file[0:5])
            consolidated_params[user_gauss_file[0:5]] = data_dict[user_gauss_file[0:5]]
    w_consolidated_gauss_params_json = gauss_users_dir + "/consolidated/consolidated_gauss_params.json"
    write_dict_to_json(consolidated_params, w_consolidated_gauss_params_json)


def write_profit_weight_to_json(list, json_to_write):
    df_params = pd.Series(list).to_frame("profit_weight")
    print(df_params)
    result = df_params.to_json(orient="index")
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))


if __name__ == "__main__":
    main()
