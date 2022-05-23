import json
import pandas as pd


def main():
    user_list = ["user1", "user2"]
    df = pd.read_json('user1_params.json')
    print(df)
    # f = open('user1_params.json')
    # data = json.load(f)
    # f = open('user2_params.json')
    # data = json.load(f)
    # print(data)


if __name__ == "__main__":
    main()
