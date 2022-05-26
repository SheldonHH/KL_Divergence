import json
import pandas as pd
from scipy.integrate import quad
import numpy as np

r_consolidated_params_json = '../data/server_joint/consolidated/consolidated_gauss_params.json'
w_consolidated_percent_json = '../data/server_joint/consolidated/consolidated_entropysum_percent.json'


def write_dict_to_json(dict, json_to_write):
    df_params = pd.DataFrame.from_dict({k: [v] for k, v in dict.items(
    )}, orient="index", columns=["user profit percentage"])
    result = df_params.to_json()
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))


def gauss(x, mu, sigma, A):
    return A*np.exp(-(x-mu)**2/2/sigma**2)


def multi_bimodal(x, *params):
    print("*params", params)
    print("type(*params)", type(params))
    gausses = 0
    paramssss = params
    print("[0][0:3]", *params[0])
    index = 0
    gauss_index = int(len(*params)/3)
    for i in range(gauss_index):
        # print("i::",i)
        gausses += gauss(x, *params[0][0+index*3:3+index*3])
        index += 1

    return gausses


def integrand(x, a, b):
    return a*x**2 + b


def main():
    #   args = sys.argv[1:]
    #   print(args)
    #   raw_data_path1 = args[0]
    #   middle_index = args[0].rindex('/')
    #   last_index = len(args[0])-1
    #   first_half = args[0][0:middle_index+1]
    #   before_extension_half = args[0][middle_index+1: args[0].rindex('.')]
    #   print("before_extension_half",)
    users_list = ["user1","user2"]
    user_entropies_dict = {}
    user_entrosum_dict = {}
    total_entrosum = 0
    f = open(r_consolidated_params_json)
    data = json.load(f)
    for user_str in users_list:
        server_joint_entropy = []
        for subkey in data[user_str].keys():
            this_d_data = data[user_str][subkey][list(
                data[user_str][subkey].keys())[0]]
            print(user_str, subkey, this_d_data)
            d_min = data[user_str][subkey]["min"]
            d_max = data[user_str][subkey]["max"]
            print(d_max)
            I = quad(multi_bimodal, d_min, d_max,  args=(list(this_d_data)))
            server_joint_entropy.append(I[0])
        print("server_joint_entropy", server_joint_entropy)
        user_entropies_dict[user_str] = server_joint_entropy
        user_entrosum_dict[user_str] = sum(server_joint_entropy)
        total_entrosum += sum(server_joint_entropy)
    print("user_entropies_dict", user_entropies_dict)
    percent_dict = {}
    for key in user_entrosum_dict.keys():
        new_value = float(user_entrosum_dict[key]) / total_entrosum
        percent_dict[key] = new_value
    print("percent_dict", percent_dict)
    write_dict_to_json(percent_dict, w_consolidated_percent_json)


if __name__ == "__main__":
    main()
