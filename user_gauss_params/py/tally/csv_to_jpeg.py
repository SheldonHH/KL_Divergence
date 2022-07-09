from numpy import genfromtxt
import numpy as np
from PIL import Image
import sys
import imageio


def image_to_vector(length_size, image: np.ndarray) -> np.ndarray:
    return image.reshape((length_size * 28 * 28, 1))


def csv_to_jpeg(numpy_array, raw_csv_argv, index_of_image):
    args = raw_csv_argv
    print(args)
    # user_1_data
    raw_csv_path1 = args[0]
    my_data = numpy_array
    # my_data = genfromtxt(raw_csv_path1, delimiter=',', skip_header=1)
    path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    username = raw_csv_path1[raw_csv_path1.rindex(
        '/')+1: raw_csv_path1.rindex('.')]
    imageio.imwrite(path+username+"_"+index_of_image+".jpeg", my_data)
    return len(my_data)
