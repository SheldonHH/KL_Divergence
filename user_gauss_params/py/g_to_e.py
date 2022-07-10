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



def main():
  individual_gauss = ["/root/KL_Divergence/user_gauss_params/data/users_individual_gauss"] # location where stores individual gauss
  directory = individual_gauss[0]
  users_list = ["user_1", "user_4"]
  subfolders = [x[0] for x in os.walk(directory)]
  print(subfolders)
  print(len(subfolders))
  for subf in subfolders:
    server_consolidate([subf], users_list)
  # calculate_entropy_golang.calculate_entropy(individual_gauss)


if __name__ == "__main__":
    main()