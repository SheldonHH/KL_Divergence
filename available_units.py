import numpy as np
import itertools
import csv
import json

raw_data_path = 'data_sample/user_1_data.csv'
freq_data_path = 'data_sample/joint/joint_frequency_1.csv'

w_counter_parti_trimmed_dict_json_path = 'data_sample/dict/counter_dict.json'
w_parti_trimmed_dict_json_path = 'data_sample/dict/sample_unit_dict.json'

partition_size = 6
counter_dict = {}
units_dict = {}


def write_second_third_dict():
    with open(w_parti_trimmed_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(units_dict))
    with open(w_counter_parti_trimmed_dict_json_path, 'w') as convert_file:
        convert_file.write(json.dumps(counter_dict))


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
    print(y_freq.size)

    lower_bound_x1 = min(p)
    lower_bound_x2 = min(q)

    for y in range(partition_size):
        for x in range(partition_size):
            lower_bound_x1 = min(p)+(x)*p_step
            lower_bound_x2 = min(q)+(y)*q_step
            upper_bound_x1 = min(p)+(x+1)*p_step
            upper_bound_x2 = min(q)+(y+1)*q_step
            strkey = str(lower_bound_x1) + "," + str(lower_bound_x2) + \
                " <= trimmed_points < " + str(upper_bound_x1) + \
                "," + str(upper_bound_x2)
            counter = 0
            sample_units = []
            print(min(p)+(x+1)*p_step, min(q)+(x+1)*q_step)
            freq_index_counter = 0
            for z in range(y_freq.size):
                freq_list = []
                if x_freq[z] >= lower_bound_x1 and y_freq[z] >= lower_bound_x2 and x_freq[z] < upper_bound_x1 and y_freq[z] < upper_bound_x2:
                    counter += 1
                    freq_list.append(x_freq[freq_index_counter])
                    freq_list.append(y_freq[freq_index_counter])
                freq_index_counter += 1
                if len(freq_list) != 0:
                    sample_units.append(freq_list)
            counter_dict[strkey] = counter
            units_dict[strkey] = sample_units

    print(counter_dict)
    np.save('unit_selection.npy', counter_dict)
    np.save('sample_units.npy', sample_units)

    write_second_third_dict()


if __name__ == "__main__":
    main()
