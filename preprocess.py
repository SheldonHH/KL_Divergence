import csv
raw_data_path = 'data_sample/user_1_data.csv'
trimmed_data_path = 'data_sample/trimmed_user_1_data.csv'


def read_from_csv():
    file_to_write = open(trimmed_data_path, 'w')
    writer = csv.writer(file_to_write)
    writer.writerow(['x', 'y'])  # write header

    file = open(raw_data_path)
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    print(header)
    rows = []
    for row in csvreader:
        rows.append(row)
        # trimmed_x = float("{:.2f}".format(row[0]))
        trimmed_x = round(float(row[0]), 1)
        trimmed_y = round(float(row[1]), 1)
        print(trimmed_x)
        print(trimmed_y)
        writer.writerow([trimmed_x, trimmed_y])


# print("{:.2f}".format(round(a, 2)))


def main():
    read_from_csv()


if __name__ == "__main__":

    main()
