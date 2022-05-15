import numpy as np
import itertools
import csv
import pandas as pd

raw_data_path = 'data_sample/user_1_data.csv'
freq_data_path = 'data_sample/joint/joint_frequency_1.csv'

w_counter_dict_path = 'data_sample/gauss_params/counter_dict.csv'
w_sample_unit_path = 'data_sample/gauss_params/sample_unit_dict.csv'

partition_size = 6
counter_dict = {}
units_dict = {}


def write_to_file():
    # with open(w_sample_unit_path, "wb") as f:
    #     writer = csv.writer(f)
    #     for i in range(len(sample_units)):
    #         writer.writerows(sample_units[i])
    # print(type(sample_units))
    print(units_dict)
    # df = pd.DataFrame(sample_units)  # construct data frame and transpose

    # df.to_csv(w_sample_unit_path, header=False, index=False)
    # file_to_write = open(data_y_frequency_path, 'w')
    # file_to_write.write(df['y'].value_counts().to_csv(header=False))

    # print(type(counter_dict))
    # print(counter_dict)
    # df = pd.DataFrame(w_sample_unit_path)
    # df.to_csv(w_sample_unit_path)

    #     for i in range(len(sample_units)):
    #         # for j in range(len(sample_units[i])):
    #         row = sample_units[i]
    #         writer.writerow(row)
    #         # writer.writerows(sample_units[i])


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
            lower_bound_x2 = min(q)+(x)*q_step
            upper_bound_x1 = min(p)+(x+1)*p_step
            upper_bound_x2 = min(q)+(x+1)*q_step
            strkey = str(lower_bound_x1) + "," + str(lower_bound_x2) + \
                "," + str(upper_bound_x1) + "," + str(upper_bound_x2)
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

    write_to_file()


if __name__ == "__main__":
    main()
