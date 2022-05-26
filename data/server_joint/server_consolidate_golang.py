import json
import pandas as pd

w_consolidated_gauss_params_json = './consolidated/consolidated_gauss_params.json'


def write_dict_to_json(dict, json_to_write):
    df_params = pd.DataFrame.from_dict(dict)
    result = df_params.to_json(orient="columns")
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))


def main():
    # args = sys.argv[1:]
    # raw_data_path1 = args[0]
    # middle_index = args[0].rindex('/')
    # last_index = len(args[0])-1
    consolidated_params = {}
    users_list = ["user1", "user2"]
    for user in users_list:
        params_file_user = user+'_params.json'
        with open(params_file_user) as json_file:
            data_dict = json.load(json_file)
        consolidated_params[user] = data_dict[user]

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
