from numpy import genfromtxt
import numpy as np
from PIL import Image
import sys
import imageio
def image_to_vector(length_size,image: np.ndarray) -> np.ndarray:
    return image.reshape((length_size * 28 * 28, 1))


def main():
    args = sys.argv[1:]
    print(args)
    # user_1_data
    raw_csv_path1 = args[0]
    my_data = genfromtxt(raw_csv_path1, delimiter=',', skip_header=1)
    
    # image_to_vector(len(my_data),my_data).save("user_1.jpeg")
    imageio.imwrite("user_1.jpeg", my_data)
    # with open("user_1.jpg", 'wb') as fh:
    #   fh.write(my_data)

    # middle_index = args[0].rindex('/')
    # last_index = len(args[0])-1
    # first_half = args[0][0:middle_index+1]
    # print("first_half", first_half) # user_4
    # second_half = args[0][middle_index+1: len(args[0])] 
    # print(second_half)
    # print(args[0].rindex('/'))
    # w_rounded_data_path1 = first_half+"features/rounded_"+second_half
    # middle_index =raw_csv_path1.rindex('/')
    # last_index = len(raw_csv_path1)-1
    # first_half = raw_csv_path1[0:middle_index+1]
    # print("first_half", first_half)
    # second_half = raw_csv_path1[middle_index+1: len(raw_csv_path1)]
    # print(second_half)
    # print(raw_csv_path1.rindex('/'))
    # w_dense_trimmed_data_path1 = first_half+"rounded_"+second_half
    # # print("w_dense_trimmed_data_path1", w_rounded_data_path1)
    # read_from_csv(raw_csv_path1, w_rounded_data_path1)
    # read_from_csv(raw_data_path2, w_dense_trimmed_data_path1)


if __name__ == "__main__":
    main()
