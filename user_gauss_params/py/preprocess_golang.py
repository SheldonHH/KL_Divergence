import csv
import sys
import json
# raw_data_path1 = 'data/user_1_data.csv'
raw_data_path2 = 'data/user_2_data.csv'
# w_trimmed_data_path1 = 'data/trimmed/trimmed_user_1_data.csv'
# w_trimmed_data_path2 = 'data/trimmed/trimmed_user_2_data.csv'
# w_dense_trimmed_data_path1 = 'data/trimmed/dense_trimmed_user_1_data.csv'
w_dense_trimmed_data_path2 = 'data/trimmed/dense_trimmed_user_2_data.csv'
# w_first_dict_json_path = 'data/dict/first_dict_data.json'
first_layer_dict = {}


def trim_row(row):
    return [int(float(row[0])), int(float(row[1]))]
    # round(float(row[1]), 1)


def dense_trim_row(row):
    # return [round(float(row[0]), 2), round(float(row[1]), 2)]
    return [round(float(row[i]),3) for i in range(len(row))]
    # return [round(float(row[0]), 2), round(float(row[1]), 2)]
    # round(float(row[1]), 1)


def write_first_dict():
    with open(w_first_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(first_layer_dict))


def read_from_csv(raw_data_path, trimmed_data_path):
    file_to_write = open(trimmed_data_path, 'w')
    writer = csv.writer(file_to_write)
    # write header

    file = open(raw_data_path)
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    header_to_write = header
    writer.writerow(header_to_write)
    oned_rows = []
    alld_rows = []
    for row in csvreader:
        for i in range(len(row)):
            # print("len(row)",len(row))
            # print("row[0]",row[0])
            oned_rows.append(row[i])
        alld_rows.append(oned_rows)

    for row in alld_rows:
        trimmed_row = dense_trim_row(row)
        writer.writerow(trimmed_row)
        str_key = str(trimmed_row[0])+"-"+str(trimmed_row[1])
        if str_key in first_layer_dict:
            if(trimmed_row[0] == 2 and trimmed_row[1] == 3):
                print("if")
            old_list = list(first_layer_dict[str_key] or [])
            old_list.append(row)
            first_layer_dict[str_key] = old_list
        else:
            new_row = []
            new_row = new_row.append(row)
            # if(trimmed_row[0] == 2 and trimmed_row[1] == 3):
            #     print("else")
            #     print(row)
            #     print(new_row)
            # TODO directly added the row, no need append()
            new_row = []
            new_row.append(row)
            first_layer_dict[str_key] = new_row
            if(trimmed_row[0] == 2 and trimmed_row[1] == 3):
                print("else")
                # print(first_layer_dict[str_key])
        # if(trimmed_row[0] == 2 and trimmed_row[1] == 3):
        #     print(first_layer_dict[str_key])
        #     break

    filtered = {k: v for k, v in first_layer_dict.items() if v is not None}
    first_layer_dict.clear()
    first_layer_dict.update(filtered)
    # print(first_layer_dict["2-3"])
    # write_first_dict()


def main():
    args = sys.argv[1:]
    print(args)
    # user_1_data
    raw_data_path1 = args[0]
    middle_index = args[0].rindex('/')
    last_index = len(args[0])-1
    first_half = args[0][0:middle_index+1]
    print("first_half", first_half)
    second_half = args[0][middle_index+1: len(args[0])]
    print(second_half)
    print(args[0].rindex('/'))
    w_dense_trimmed_data_path1 = first_half+"trimmed/dense_trimmed_"+second_half
    print("w_dense_trimmed_data_path1", w_dense_trimmed_data_path1)
    read_from_csv(raw_data_path1, w_dense_trimmed_data_path1)
    # read_from_csv(raw_data_path2, w_dense_trimmed_data_path1)


if __name__ == "__main__":
    main()
