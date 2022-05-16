import numpy as np
import itertools
import csv
import json
from collections import Counter

raw_data_path = 'data_sample/user_1_data.csv'
freq_data_path = 'data_sample/joint/joint_frequency_1.csv'

w_counter_parti_trimmed_dict_json_path = 'data_sample/dict/counter_parti_dict.json'
w_parti_trimmed_dict_json_path = 'data_sample/dict/trimmed_list_parti_dict.json'
w_sum_parti_trimmed_dict_json_path = 'data_sample/dict/sum_parti_dict.json'
w_selected_avg_parti_trimmed_dict_json_path = 'data_sample/dict/selected_avg_parti_dict.json'

sample_min_threshold_percent = 10
partition_size = 6
counter_dict = {}
units_dict = {}
parit_sum_dict = {}
selected__parit_avg_dict = {}


def create_avg_dict():
    for key in counter_dict.keys():
        if(int(counter_dict[key]) >= sample_min_threshold_percent):
            avg_value_x1 = float(
                parit_sum_dict[key][0]) / float(counter_dict[key])
            avg_value_x2 = float(
                parit_sum_dict[key][1]) / float(counter_dict[key])
            avg_key_x1 = (float(key.split(",")[0])+float(key.split(",")[2]))/2
            avg_key_x2 = (float(key.split(",")[1])+float(key.split(",")[3]))/2
            str_avg_key = str(avg_key_x1)+","+str(avg_key_x2)
            selected__parit_avg_dict[str_avg_key] = [
                avg_value_x1, avg_value_x2]
    print(len(selected__parit_avg_dict))


def write_second_third_dict():
    with open(w_parti_trimmed_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(units_dict))
    with open(w_counter_parti_trimmed_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(counter_dict))
    with open(w_sum_parti_trimmed_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(parit_sum_dict))
    with open(w_selected_avg_parti_trimmed_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(selected__parit_avg_dict))


def main():
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
            lower_bound_x2 = min(q)+(y)*q_step
            upper_bound_x1 = min(p)+(x+1)*p_step
            upper_bound_x2 = min(q)+(y+1)*q_step
            strkey = str(lower_bound_x1) + "," + str(lower_bound_x2) + \
                "," + str(upper_bound_x1) + \
                "," + str(upper_bound_x2)
            #  <= trimmed_points <
            counter = 0
            parti_sum_x1 = 0
            parti_sum_x2 = 0
            sample_units = []
            freq_index_counter = 0
            for z in range(y_freq.size):
                freq_list = []
                if x_freq[z] >= lower_bound_x1 and y_freq[z] >= lower_bound_x2 and x_freq[z] < upper_bound_x1 and y_freq[z] < upper_bound_x2:
                    counter += 1
                    freq_list.append(x_freq[freq_index_counter])
                    freq_list.append(y_freq[freq_index_counter])
                    parti_sum_x1 += x_freq[z]
                    parti_sum_x2 += y_freq[z]
                freq_index_counter += 1
                if len(freq_list) != 0:
                    sample_units.append(freq_list)
            counter_dict[strkey] = counter
            units_dict[strkey] = sample_units
            parit_sum_dict[strkey] = [parti_sum_x1, parti_sum_x2]

    create_avg_dict()
    write_second_third_dict()


if __name__ == "__main__":
    main()
