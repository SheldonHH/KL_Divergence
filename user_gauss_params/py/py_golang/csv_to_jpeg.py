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
    path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    username = raw_csv_path1[raw_csv_path1.rindex('/')+1: raw_csv_path1.rindex('.')]
    imageio.imwrite(path+username+".jpeg", my_data)

if __name__ == "__main__":
    main()
