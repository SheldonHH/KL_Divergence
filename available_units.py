from distutils.command.build_scripts import first_line_re
import numpy as np
import itertools
import csv
import json
from collections import Counter
from random import sample
from itertools import chain

raw_data_path = 'data_sample/user_1_data.csv'
freq_data_path = 'data_sample/joint/joint_frequency_1.csv'
first_layer_dict_json_path = 'data_sample/dict/first_dict_data.json'

w_counter_parti_trimmed_dict_json_path = 'data_sample/dict/second_process_json/counter_parti_dict.json'
w_parti_trimmed_dict_json_path = 'data_sample/dict/second_process_json/trimmed_list_parti_dict.json'
w_parti_extended_dict_json_path = 'data_sample/dict/second_process_json/extended_list_parti_dict.json'
w_sum_parti_trimmed_dict_json_path = 'data_sample/dict/second_process_json/sum_parti_dict.json'
w_selected_avg_parti_trimmed_dict_json_path = 'data_sample/dict/second_process_json/selected_avg_parti_dict.json'  # without freq

# (x1, x2, freq) prepare for 2D gauss
w_selected_avg_parti_trimmed_dict_path = 'data_sample/dict/prepare_for_gauss/selected_avg_parti_dict.csv'
w_sample_selected_avg_parti_trimmed_dict_path = 'data_sample/dict/prepare_for_gauss/sample_selected_avg_parti_dict.csv'
w_extended_sample_selected_avg_parti_trimmed_dict_path = 'data_sample/dict/prepare_for_gauss/extended_sample_selected_avg_parti_dict.csv'

# percent in decimal
sample_min_threshold_percent = 1
partition_size = 6
counter_dict = {}
units_dict = {}
extended_units_dict = {}
parit_sum_dict = {}
selected__parit_avg_dict = {}
sample_selected__parit_avg_dict = {}
extended_sample_selected__parit_avg_dict = {}


def load_first_layer_dict():
    f = open(first_layer_dict_json_path,)
    return json.load(f)
    # print(first_layer_dict)


def create_avg_dict():
    for key in counter_dict.keys():
        if(sample_min_threshold_percent*int(counter_dict[key]) >= 1):
            avg_value_x1 = float(
                parit_sum_dict[key][0]) / float(counter_dict[key])
            avg_value_x2 = float(
                parit_sum_dict[key][1]) / float(counter_dict[key])
            avg_key_x1 = (float(key.split(",")[0])+float(key.split(",")[2]))/2
            avg_key_x2 = (float(key.split(",")[1])+float(key.split(",")[3]))/2
            str_avg_key = str(avg_key_x1)+","+str(avg_key_x2)
            selected__parit_avg_dict[str_avg_key] = [
                avg_value_x1, avg_value_x2]
    # print(len(selected__parit_avg_dict))


def Average(lst):
    return sum(lst) / len(lst)


def create_sample_sum_avg_dict():
    for key in counter_dict.keys():
        if(sample_min_threshold_percent*len(units_dict[key]) >= 1):
            sample_list = sample(
                units_dict[key], sample_min_threshold_percent*len(units_dict[key]))
            # print(sample_list)
            avg_value_x1 = Average(sample_list[0])
            avg_value_x2 = Average(sample_list[1])
            avg_key_x1 = (float(key.split(",")[0])+float(key.split(",")[2]))/2
            avg_key_x2 = (float(key.split(",")[1])+float(key.split(",")[3]))/2
            str_avg_key = str(avg_key_x1)+","+str(avg_key_x2)
            sample_selected__parit_avg_dict[str_avg_key] = [
                avg_value_x1, avg_value_x2]
    # print(len(sample_selected__parit_avg_dict))


def create_extended_sample_sum_avg_dict():
    misalign_counter = 0
    correct_counter = 0
    for key in counter_dict.keys():
        if(sample_min_threshold_percent*len(extended_units_dict[key]) >= 1):
            if len(units_dict[key]) != int(counter_dict[key]):
                print("wrong")
            if len(units_dict[key]) > len(extended_units_dict[key]):
                print(key)
                print("extended_unit", len(extended_units_dict[key]))
                print("unit", len(units_dict[key]))
                misalign_counter += 1
                print(key)
                print(extended_units_dict[key])
                print(units_dict[key])
                break
            else:
                correct_counter += 1
        # print("misalign_counter", misalign_counter)
        # print("correct_counter", correct_counter)
        sample_list = sample(
            extended_units_dict[key], sample_min_threshold_percent*len(extended_units_dict[key]))
        # print(sample_list)
        avg_value_x1 = Average(list(np.float_([i[0] for i in sample_list])))
        avg_value_x2 = Average(list(np.float_([i[1] for i in sample_list])))
        # avg_value_x2 = Average(list(np.float_(sample_list[1])))
        # print([i[1] for i in sample_list])
        avg_key_x1 = (float(key.split(",")[0])+float(key.split(",")[2]))/2
        avg_key_x2 = (float(key.split(",")[1])+float(key.split(",")[3]))/2
        str_avg_key = str(avg_key_x1)+","+str(avg_key_x2)
        extended_sample_selected__parit_avg_dict[str_avg_key] = [
            avg_value_x1, avg_value_x2]


def write_second_third_dict():
    with open(w_parti_trimmed_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(units_dict))
    with open(w_parti_extended_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(extended_units_dict))
    with open(w_counter_parti_trimmed_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(counter_dict))
    with open(w_sum_parti_trimmed_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(parit_sum_dict))
    # with open(w_selected_avg_parti_trimmed_dict_json_path, 'w') as convert_file:
    #     convert_file.write(json.dumps(selected__parit_avg_dict))

    # without sample
    with open(w_selected_avg_parti_trimmed_dict_path, 'w') as f:
        writer = csv.writer(f)
        header_to_write = ['x1', 'x2', 'freq']
        writer.writerow(header_to_write)
        for value in selected__parit_avg_dict.values():
            value.append(1)
            writer.writerow(value)

    # sample based on filtered data
    with open(w_sample_selected_avg_parti_trimmed_dict_path, 'w') as f:
        writer = csv.writer(f)
        header_to_write = ['x1', 'x2', 'freq']
        writer.writerow(header_to_write)
        for value in sample_selected__parit_avg_dict.values():
            value.append(1)
            writer.writerow(value)

    # sample based on raw data
    with open(w_extended_sample_selected_avg_parti_trimmed_dict_path, 'w') as f:
        writer = csv.writer(f)
        header_to_write = ['x1', 'x2', 'freq']
        writer.writerow(header_to_write)
        for value in extended_sample_selected__parit_avg_dict.values():
            value.append(1)
            writer.writerow(value)


def main():
    first_layer_dict = load_first_layer_dict()
    # print(first_layer_dict)
    # calculate the kl divergence
    data = np.loadtxt(raw_data_path, delimiter=',', skiprows=1)
    p = data[:, 0]
    q = data[:, 1]
    p_step = (max(p) - min(p))/partition_size
    q_step = (max(q) - min(q))/partition_size

    joint_frequency = np.loadtxt(freq_data_path, delimiter=',', skiprows=1)

    x_freq = joint_frequency[:, 0]
    y_freq = joint_frequency[:, 1]

    lower_bound_x1 = min(p)
    lower_bound_x2 = min(q)

    for y in range(partition_size):
        for x in range(partition_size):
            lower_bound_x1 = min(p)+(x)*p_step
            upper_bound_x1 = min(p)+(x+1)*p_step
            lower_bound_x2 = min(q)+(y)*q_step
            upper_bound_x2 = min(q)+(y+1)*q_step
            strkey = str(lower_bound_x1) + "," + str(upper_bound_x1) + \
                "," + str(lower_bound_x2) + \
                "," + str(upper_bound_x2)
            #  <= trimmed_points <
            counter = 0
            parti_sum_x1 = 0
            parti_sum_x2 = 0
            sample_units = []
            extended_sample_units = []
            freq_index = 0
            for freq_index in range(y_freq.size):
                freq_list = []
                if x_freq[freq_index] >= lower_bound_x1 and x_freq[freq_index] < upper_bound_x1 and y_freq[freq_index] >= lower_bound_x2 and y_freq[freq_index] < upper_bound_x2:
                    counter += 1
                    freq_list.append(x_freq[freq_index])
                    freq_list.append(y_freq[freq_index])
                    first_layer_strkey = str(int(x_freq[freq_index])) + \
                        "-"+str(int(y_freq[freq_index]))
                    parti_sum_x1 += x_freq[freq_index]
                    parti_sum_x2 += y_freq[freq_index]

                    for key in first_layer_dict.keys():
                        if first_layer_strkey == key:
                            extended_sample_units.append(
                                first_layer_dict[first_layer_strkey])
                if len(freq_list) != 0:
                    sample_units.append(freq_list)
            counter_dict[strkey] = counter
            units_dict[strkey] = sample_units
            # if len(extended_sample_units) != 0:
            flatten_list = list(chain.from_iterable(extended_sample_units))
            extended_units_dict[strkey] = flatten_list
            parit_sum_dict[strkey] = [parti_sum_x1, parti_sum_x2]

    create_avg_dict()
    create_sample_sum_avg_dict()  # sample% then calculate the avg

    create_extended_sample_sum_avg_dict()
    write_second_third_dict()


if __name__ == "__main__":
    main()
