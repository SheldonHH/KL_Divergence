import pandas as pd
import sidetable
import csv
import json
trimmed_data_path = 'data_sample/trimmed_user_1_data.csv'
dense_trimmed_data_path = 'data_sample/trimmed/dense_trimmed_user_1_data.csv'
# data_x1_frequency_path = 'data_sample/independent/x1_frequency_user_1_data.csv'
# data_x2_frequency_path = 'data_sample/independent/x2_frequency_user_1_data.csv'


each_col_json_data_frequency_path = 'data_sample/independent/each_col_frequency_user1_data.json'
json_data_x1_frequency_path = 'data_sample/independent/x1_frequency_user_1_data.json'
json_data_x2_frequency_path = 'data_sample/independent/x2_frequency_user_1_data.json'


def read_from_csv():
    df = pd.read_csv(dense_trimmed_data_path)
    # print(df['x1'].value_counts())
    # print(df['x2'].value_counts())
    # write_to_csv(df)
    # print("df.to_dict()", df.to_dict())
    write_to_json(df)

#  Write to Json Format

# writer.writerow(x2_frequence)


# def write_to_csv(df):
#     file_to_write = open(data_x1_frequency_path, 'w')
#     writer = csv.writer(file_to_write)

#     print("df['x1'].value_counts()",df['x1'].value_counts())
#     print("tyoe   df['x1'].value_counts()",  type(df['x1'].value_counts()))
#     file_to_write.write(df['x1'].value_counts().to_csv(header=False))

#     file_to_write = open(data_x2_frequency_path, 'w')
#     file_to_write.write(df['x2'].value_counts().to_csv(header=False))


def write_to_json(df):
    json_file_to_write = open(each_col_json_data_frequency_path, 'w')
    # json_file_to_write.write(json.dumps(df['x1'].value_counts().to_dict()))
    trimmed_dict = df.to_dict()
    each_col_freq_dict = {}
    for key, value in trimmed_dict.items():
        each_col_freq_dict[key] = pd.DataFrame.from_dict(value, orient='index').value_counts().to_dict()
        print(pd.DataFrame.from_dict(value, orient='index').value_counts())
        # print("key", ''.join(key))
        # print("fds",pd.Series(value).to_frame(''.join(key)).value_counts().to_dict())
        # each_col_freq_dict[''.join(key)]=pd.Series(value).to_frame(''.join(key)).value_counts().to_dict()
    print(each_col_freq_dict)


    final_col_freq_dict = {}
    for bigger_key,bigger_value in each_col_freq_dict.items():
        col_freq_dict = {}
        for key, value in bigger_value.items():
            col_freq_dict[key[0]] = value  
        final_col_freq_dict[bigger_key] = col_freq_dict
    json_file_to_write.write(json.dumps(final_col_freq_dict))




def main():
    read_from_csv()


if __name__ == "__main__":

    main()
