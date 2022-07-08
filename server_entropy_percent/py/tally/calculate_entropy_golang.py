import json
import pandas as pd
from scipy.integrate import quad
import scipy.stats
import numpy as np
import sys


# def mean_confidence_interval(data, confidence=0.95):
#     a = 1.0 * np.array(data)
#     n = len(a)
#     m, se = np.mean(a), scipy.stats.sem(a)
#     h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
#     return m, m-h, m+h


def write_dict_to_json(dict, json_to_write):
    df_params = pd.DataFrame.from_dict({k: [v] for k, v in dict.items(
    )}, orient="index", columns=["user profit percentage"])
    result = df_params.to_json()
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))


def gauss(x, mu, sigma, A):
    return A*np.exp(-(x-mu)**2/2/sigma**2)


def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros


def multi_bimodal(x, *params):
    gausses = 0
    gauss_index = int(len(*params)/3)
    for i in range(gauss_index):
        gausses += weights_array[i]*gauss(x, *params[0][0+i*3:3+i*3])
    return gausses


def integrand(x, a, b):
    return a*x**2 + b

# weights_array = []


def calculate_entropy(individual_gauss):
    args = individual_gauss
    gauss_users_dir = args[0]
    print("before_extension_half",)
    users_list = ["user1", "user2"]
    user_entropies_dict = {}
    user_entrosum_dict = {}
    total_entrosum = 0
    r_consolidated_params_json = gauss_users_dir + \
        "/consolidated/consolidated_gauss_params.json"
    w_consolidated_percent_json = gauss_users_dir + \
        "/consolidated/entropysum_percent.json"
    f = open(r_consolidated_params_json)
    data = json.load(f)
    for user_str in data.keys():
        print("user_key", user_str)
        users_individual_gauss_entropy = []
        this_d_data = data[user_str]["gauss"]
        print("F35555", this_d_data)
        d_min = data[user_str]["min"]
        d_max = data[user_str]["max"]
        print(d_max)
        global weights_array
        weights_array = data[user_str]["weights"]
        I = quad(multi_bimodal, d_min, d_max, args=(list(this_d_data)))
        print("I", I)
        users_individual_gauss_entropy.append(
            data[user_str]["raw_data_size"]*I[0])
        print("users_individual_gauss_entropy", users_individual_gauss_entropy)
        user_entropies_dict[user_str] = users_individual_gauss_entropy
        user_entrosum_dict[user_str] = sum(users_individual_gauss_entropy)
        total_entrosum += sum(users_individual_gauss_entropy)
    print("user_entropies_dict", user_entropies_dict)
    percent_dict = {}
    for key in user_entrosum_dict.keys():
        new_value = float(user_entrosum_dict[key]) / total_entrosum
        percent_dict[key] = new_value
    print("percent_dict", percent_dict)
    write_dict_to_json(percent_dict, w_consolidated_percent_json)
    return percent_dict
