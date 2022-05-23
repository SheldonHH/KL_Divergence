import json
import pandas as pd

w_consolidated_gauss_params_json = 'consolidated_gauss_params.json'
w_consolidated_entropies_json = 'consolidated_entropies.json'
w_consolidated_percent_json = 'consolidated_percent.json'


def write_dict_to_json(dict, json_to_write):
    df_params = pd.DataFrame.from_dict(dict)
    result = df_params.to_json(orient="columns")
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))


def main():
    consolidated_params = {}
    consolidated_entropies = {}
    consolidated_sum_entropies = 0
    users_list = ["user1", "user2"]
    for user in users_list:
        params_file_user = user+'_params.json'
        with open(params_file_user) as json_file:
            data_dict = json.load(json_file)
        consolidated_params[user] = data_dict[user]

        entropies_file_user = user+'_entropies.json'
        with open(entropies_file_user) as json_file:
            data_dict = json.load(json_file)
        consolidated_entropies[user] = data_dict[user]

        entropies_sum_file_user = user+'_entropies_sum.json'
        with open(entropies_sum_file_user) as json_file:
            data_dict = json.load(json_file)
            print(data_dict[user]["0"])
        consolidated_sum_entropies += float(data_dict[user]["0"])

    print(consolidated_params)
    print(consolidated_entropies)
    write_dict_to_json(consolidated_params, w_consolidated_gauss_params_json)
    write_dict_to_json(consolidated_entropies, w_consolidated_entropies_json)

    # weight of each user
    consolidated_percent_dict = {}
    for user in users_list:
        entropies_sum_file_user = user+'_entropies_sum.json'
        with open(entropies_sum_file_user) as json_file:
            data_dict = json.load(json_file)
            print(data_dict[user]["0"])
        consolidated_percent_dict[user] = [(
            data_dict[user]["0"])/consolidated_sum_entropies]
    write_dict_to_json(consolidated_percent_dict,
                       w_consolidated_percent_json)


if __name__ == "__main__":
    main()
