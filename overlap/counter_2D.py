from collections import Counter
import pandas as pd
import csv
trimmed_data_path = 'data_sample/trimmed_user_1_data.csv'
data_frequency_path = 'data_sample/frequency_user_1_data.csv'


def read_from_csv():
    file = open(trimmed_data_path)
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    print(header)
    rows = []

    for row in csvreader:
        rows.append(row)
    # print(Counter(map(tuple, rows)))
    print(rows)


def main():
    read_from_csv()


if __name__ == "__main__":

    main()
