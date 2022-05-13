import csv
raw_data_path1 = 'data_sample/user_1_data.csv'
raw_data_path2 = 'data_sample/user_2_data.csv'
trimmed_data_path1 = 'data_sample/trimmed/trimmed_user_1_data.csv'
trimmed_data_path2 = 'data_sample/trimmed/trimmed_user_2_data.csv'


def trim_row(row):
    return [int(float(row[0])), int(float(row[1]))]
    # round(float(row[1]), 1)


def read_from_csv(raw_data_path, trimmed_data_path):
    file_to_write = open(trimmed_data_path, 'w')
    writer = csv.writer(file_to_write)
    header_to_write = ['x', 'y']
    writer.writerow(header_to_write)
    # write header

    file = open(raw_data_path)
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    twod_rows = []
    x1_x2_col = []
    for row in csvreader:
        oned_rows = []
        oned_rows.append(row[0])
        oned_rows.append(row[1])
        twod_rows.append(oned_rows)

    for row in twod_rows:
        trimmed_row = trim_row(row)
        writer.writerow(trimmed_row)


# print("{:.2f}".format(round(a, 2)))


def main():
    read_from_csv(raw_data_path1, trimmed_data_path1)
    read_from_csv(raw_data_path2, trimmed_data_path2)


if __name__ == "__main__":
    main()
