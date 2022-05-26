import pandas as pd
import sidetable
import csv
import json
import sys

json_data_x1_frequency_path = 'data/independent/x1_frequency_user_1_data.json'
json_data_x2_frequency_path = 'data/independent/x2_frequency_user_1_data.json'


def read_from_csv(r_dense_trimmed_data_path1, freq_path):
    df = pd.read_csv(r_dense_trimmed_data_path1)
    write_to_json(df, freq_path)


def write_to_json(df, freq_path):
    json_file_to_write = open(freq_path, 'w')
    # json_file_to_write.write(json.dumps(df['x1'].value_counts().to_dict()))
    trimmed_dict = df.to_dict()
    freq_dict = {}
    for key, value in trimmed_dict.items():
        freq_dict[key] = pd.DataFrame.from_dict(
            value, orient='index').value_counts().to_dict()
        print(pd.DataFrame.from_dict(value, orient='index').value_counts())
        # print("key", ''.join(key))
        # print("fds",pd.Series(value).to_frame(''.join(key)).value_counts().to_dict())
        # freq_dict[''.join(key)]=pd.Series(value).to_frame(''.join(key)).value_counts().to_dict()
    print(freq_dict)

    final_col_freq_dict = {}
    for bigger_key, bigger_value in freq_dict.items():
        col_freq_dict = {}
        for key, value in bigger_value.items():
            col_freq_dict[key[0]] = value
        final_col_freq_dict[bigger_key] = col_freq_dict
    json_file_to_write.write(json.dumps(final_col_freq_dict))


def main():
    args = sys.argv[1:]
    print(args)
    # user_1_data
    raw_data_path1 = args[0]
    middle_index = args[0].rindex('/')
    last_index = len(args[0])-1
    first_half = args[0][0:middle_index+1]
    before_extension_half = args[0][middle_index+1: args[0].rindex('.')]
    r_dense_trimmed_data_path1 = first_half + \
        "trimmed/dense_trimmed_"+before_extension_half+".csv"
    freq_path = first_half + \
        "independent/freq_"+before_extension_half+".json"
    read_from_csv(r_dense_trimmed_data_path1, freq_path)


if __name__ == "__main__":

    main()
