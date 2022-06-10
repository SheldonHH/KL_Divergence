import csv
import sys
import json
# raw_data_path1 = 'data/user_1_data.csv'

first_layer_dict = {}


def trim_row(row):
    return [int(float(row[0])), int(float(row[1]))]
    # round(float(row[1]), 1)


def dense_trim_row(row):
    print("row****",row)
    # return [round(float(row[0]), 2), round(float(row[1]), 2)]
    return [round(float(item),1) for item in row[0]]
    # return [round(float(row[0]), 2), round(float(row[1]), 2)]
    # round(float(row[1]), 1)


def write_first_dict():
    with open(w_first_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(first_layer_dict))


def read_from_csv(raw_data_path, trimmed_data_path):

    # write header

    with open(raw_data_path, 'r') as file:
      header = []
      oned_rows = []
      alld_rows = []
      csvreader = csv.reader(file)
      for row in csvreader:
        oned_rows.append(row)
      alld_rows.append(oned_rows)
    trimmed_row = dense_trim_row(alld_rows[0])
    print(trimmed_row)
    with open(trimmed_data_path, 'w') as file_to_write:
        writer = csv.writer(file_to_write)
        for final_row in trimmed_row:
            print("final_row", final_row)
            writer.writerow([final_row])


def main():
    args = sys.argv[1:]
    print(args)
    # user_1_data
    raw_data_path1 = args[0]
    middle_index = args[0].rindex('/')
    last_index = len(args[0])-1
    first_half = args[0][0:middle_index+1]
    print("first_half", first_half) # user_4
    second_half = args[0][middle_index+1: len(args[0])] 
    print(second_half)
    print(args[0].rindex('/'))
    w_rounded_data_path1 = first_half+"features/rounded_"+second_half
    middle_index =raw_data_path1.rindex('/')
    last_index = len(raw_data_path1)-1
    first_half = raw_data_path1[0:middle_index+1]
    print("first_half", first_half)
    second_half = raw_data_path1[middle_index+1: len(raw_data_path1)]
    print(second_half)
    print(raw_data_path1.rindex('/'))
    w_dense_trimmed_data_path1 = first_half+"rounded_"+second_half
    # print("w_dense_trimmed_data_path1", w_rounded_data_path1)
    read_from_csv(raw_data_path1, w_rounded_data_path1)
    # read_from_csv(raw_data_path2, w_dense_trimmed_data_path1)


if __name__ == "__main__":
    main()
