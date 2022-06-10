import csv
import sys
import json
# raw_data_path1 = 'data/user_1_data.csv'

first_layer_dict = {}


def trim_row(row):
    return [int(float(row[0])), int(float(row[1]))]
    # round(float(row[1]), 1)


def rounding_row(rows):
    # print("row****",row)
    # return [round(float(row[0]), 2), round(float(row[1]), 2)]
    return [round(float(item[0]),1) for item in rows]
    # return [round(float(row[0]), 2), round(float(row[1]), 2)]
    # round(float(row[1]), 1)


def read_from_csv(features_path, rounded_data_path):
    with open(features_path, 'r') as file:
        header = []
        oned_rows = []
        csvreader = csv.reader(file)
        for row in csvreader:
            oned_rows.append(row)
        print("len(csvreader)",len(oned_rows))
       
    #   alld_rows.append(oned_rows)
    trimmed_row = rounding_row(oned_rows)
    print("trimmed_row",trimmed_row)
    with open(rounded_data_path, 'w') as file_to_write:
        writer = csv.writer(file_to_write)
        for final_row in trimmed_row:
            writer.writerow([final_row])


def main():
    args = sys.argv[1:]
    print(args)
    # user_1_data
    raw_csv_path1 = args[0]
    middle_index = args[0].rindex('/')
    last_index = len(args[0])-1
    first_half = args[0][0:middle_index+1]
    # print("first_half", first_half) # user_4
    second_half = args[0][middle_index+1: len(args[0])] 
    print(second_half)
    print(args[0].rindex('/'))

    path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    username = raw_csv_path1[raw_csv_path1.rindex('/')+1: raw_csv_path1.rindex('.')]
    r_features_csv = path+username+"_features.csv"
    w_rounded_data_path1 = first_half+"features/rounded_"+second_half
    # print("w_dense_rounded_data_path1", w_rounded_data_path1)
    read_from_csv(r_features_csv, w_rounded_data_path1)
    # read_from_csv(raw_data_path2, w_dense_rounded_data_path1)


if __name__ == "__main__":
    main()
