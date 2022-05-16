import pandas as pd
import sidetable
import csv
import json
trimmed_data_path1 = 'data_sample/trimmed/trimmed_user_1_data.csv'
trimmed_data_path2 = 'data_sample/trimmed/trimmed_user_2_data.csv'
joint_frequency_path1 = 'data_sample/joint/joint_frequency_1.csv'
joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'
# data_y_frequency_path = 'data_sample/y_frequency_user_1_data.csv'
# json_data_x_frequency_path = 'data_sample/x_frequency_user_1_data.json'
# json_data_y_frequency_path = 'data_sample/y_frequency_user_1_data.json'


def read_from_csv(trimmed_data_path, joint_frequency_path):
    df = pd.read_csv(trimmed_data_path)
    # print(df['x'].value_counts())
    # print(df['y'].value_counts())
    write_to_csv(df, joint_frequency_path)
    # write_to_json(df)

#  Write to Json Format

# writer.writerow(y_frequence)


def write_to_csv(df, joint_frequency_path):
    file_to_write = open(joint_frequency_path, 'w')
    writer = csv.writer(file_to_write)
    file_to_write.write(df.value_counts(['x', 'y']).to_csv())

    # file_to_write = open(data_y_frequency_path, 'w')
    # file_to_write.write(df['y'].value_counts().to_csv(header=False))


# def write_to_json(df):
#     json_file_to_write = open(json_data_x_frequency_path, 'w')
#     json_file_to_write.write(json.dumps(df['x'].value_counts().to_dict()))
#     json_file_to_write = open(json_data_y_frequency_path, 'w')
#     json_file_to_write.write(json.dumps(df['y'].value_counts().to_dict()))


def main():
    read_from_csv(trimmed_data_path1, joint_frequency_path1)
    read_from_csv(trimmed_data_path2, joint_frequency_path2)


if __name__ == "__main__":

    main()
