import pandas as pd
import sidetable
import csv
import json
trimmed_data_path = 'data_sample/trimmed_user_1_data.csv'
data_x_frequency_path = 'data_sample/x_frequency_user_1_data.csv'
data_y_frequency_path = 'data_sample/y_frequency_user_1_data.csv'
json_data_y_frequency_path = 'data_sample/y_frequency_user_1_data.json'


def read_from_csv():
    df = pd.read_csv(trimmed_data_path)
    print(df['x'].value_counts())
    print(df['y'].value_counts())

    file_to_write = open(data_x_frequency_path, 'w')
    writer = csv.writer(file_to_write)
    file_to_write.write(df['x'].value_counts().to_csv(header=False))

    file_to_write = open(data_y_frequency_path, 'w')
    file_to_write.write(df['y'].value_counts().to_csv(header=False))

#  Write to Json Format
    # json_file_to_write = open(json_data_y_frequency_path, 'w')
    # json_file_to_write.write(json.dumps(df['y'].value_counts().to_dict()))
    # writer = csv.writer(file_to_write)
    # writer.writerow(df['y'].value_counts().to_dict())
# writer.writerow(y_frequence)


def main():
    read_from_csv()


if __name__ == "__main__":

    main()
