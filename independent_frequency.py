import pandas as pd
import sidetable
import csv
import json
trimmed_data_path = 'data_sample/trimmed_user_1_data.csv'
dense_trimmed_data_path = 'data_sample/trimmed/dense_trimmed_user_1_data.csv'
data_x1_frequency_path = 'data_sample/independent/x1_frequency_user_1_data.csv'
data_x2_frequency_path = 'data_sample/independent/x2_frequency_user_1_data.csv'
json_data_x1_frequency_path = 'data_sample/independent/x1_frequency_user_1_data.json'
json_data_x2_frequency_path = 'data_sample/independent/x2_frequency_user_1_data.json'


def read_from_csv():
    df = pd.read_csv(dense_trimmed_data_path)
    # print(df['x1'].value_counts())
    # print(df['x2'].value_counts())
    write_to_csv(df)
    write_to_json(df)

#  Write to Json Format

# writer.writerow(x2_frequence)


def write_to_csv(df):
    file_to_write = open(data_x1_frequency_path, 'w')
    writer = csv.writer(file_to_write)
    file_to_write.write(df['x1'].value_counts().to_csv(header=False))

    file_to_write = open(data_x2_frequency_path, 'w')
    file_to_write.write(df['x2'].value_counts().to_csv(header=False))


def write_to_json(df):
    json_file_to_write = open(json_data_x1_frequency_path, 'w')
    json_file_to_write.write(json.dumps(df['x1'].value_counts().to_dict()))
    json_file_to_write = open(json_data_x2_frequency_path, 'w')
    json_file_to_write.write(json.dumps(df['x2'].value_counts().to_dict()))


def main():
    read_from_csv()


if __name__ == "__main__":

    main()
