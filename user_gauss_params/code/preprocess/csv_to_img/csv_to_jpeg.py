
import numpy as np
import imageio
import os


def image_to_vector(length_size, image: np.ndarray) -> np.ndarray:
    return image.reshape((length_size * 28 * 28, 1))


def csv_to_jpeg(numpy_array, raw_csv_argv, index_of_image, preprocess_alias):
    args = raw_csv_argv
    print(args)
    # user_1_data
    raw_csv_path1 = args[0]
    my_data = numpy_array
    path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    preprocess_alias = raw_csv_path1[raw_csv_path1.rindex(
        '/')+1: raw_csv_path1.rindex('.')]

    dir_str = path+"image/"+preprocess_alias+"/"
    if os.path.isdir(dir_str) == False:
        os.mkdir(dir_str) # make dir for that user

    imageio.imwrite(dir_str+preprocess_alias+"_"+index_of_image+".jpeg", my_data)
    return len(my_data)