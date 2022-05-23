import json


def main():
    consolidated_params = {}
    consolidated_entropies = {}
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

    print(consolidated_params)
    print(consolidated_entropies)


if __name__ == "__main__":
    main()
