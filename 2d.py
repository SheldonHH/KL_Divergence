from re import T
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Parameters, minimize, report_fit
from scipy.interpolate import griddata
import math


def gaussian2D(x, y, cen_x, cen_y, sig_x, sig_y, offset):
    return np.exp(-(((cen_x-x)/sig_x)**2 + ((cen_y-y)/sig_y)**2)/2.0) + offset


def residuals(p, x, y, z):
    height = p["height"].value
    cen_x = p["centroid_x"].value
    cen_y = p["centroid_y"].value
    sigma_x = p["sigma_x"].value
    sigma_y = p["sigma_y"].value
    offset = p["background"].value
    return (z - height*gaussian2D(x, y, cen_x, cen_y, sigma_x, sigma_y, offset))


joint_frequency_path1 = 'data_sample/joint/joint_frequency_1.csv'
joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'
w_twod_gauss_params_txt_path1 = 'data_sample/gauss_params/2d_gauss_1.txt'
w_twod_gauss_params_txt_path2 = 'data_sample/gauss_params/2d_gauss_2.txt'

# selected_avg_parti_trimmed_dict_path = 'data_sample/dict/prepare_for_gauss/selected_avg_parti_dict.csv'
# sample_selected_avg_parti_trimmed_dict_path = 'data_sample/dict/prepare_for_gauss/sample_selected_avg_parti_dict.csv'
# w_selected_avg_gauss_params_txt_path = 'data_sample/gauss_params/selected_avg_gauss_params.txt'
# w_sample_selected_avg_gauss_params_txt_path = 'data_sample/gauss_params/sample_selected_avg_gauss_params.txt'

extend_selected_avg_parti_trimmed_dict_path = 'data_sample/dict/prepare_for_gauss/extended_sample_selected_avg_parti_dict.csv'
w_extended_selected_avg_gauss_params_txt_path = 'data_sample/gauss_params/extendedselected_avg_gauss_params.txt'

file_data1 = []
x1_list = []
x2_list = []
z_list = []


def process_data(frequency_r_path, gauss_w_path):
    file_data1 = np.loadtxt(frequency_r_path,
                            delimiter=',', skiprows=1)
    for col1, col2, col3 in file_data1:
        # sg.append([col1, col2])
        x1_list.append(col1)
        x2_list.append(col2)
        z_list.append(col3)
    fit_gaussian(gauss_w_path)


def showFig(x, y, z):
    X, Y = np.meshgrid(np.linspace(x.min(), x.max(), 1000),
                       np.linspace(y.min(), y.max(), 1000))

    Z = griddata((x, y), z, (X, Y), method='linear', fill_value=0)
    fig, ax = plt.subplots()
    art = ax.pcolor(X, Y, Z, shading='auto')
    plt.colorbar(art, ax=ax, label='z')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.show()


def fit_gaussian(gauss_w_path):
    x1_ndarray = np.asarray(x1_list, dtype=np.float32)
    x2_ndarray = np.asarray(x2_list, dtype=np.float32)
    x3_ndarray = np.asarray(z_list, dtype=np.float32)
    x, y = np.meshgrid(np.linspace(x1_ndarray.min(), x1_ndarray.max(), 100),
                       np.linspace(x2_ndarray.min(), x2_ndarray.max(), 100))

    arr = np.stack((x1_ndarray, x2_ndarray), axis=1)
    # weighted arithmetic mean (corrected - check the section below)
    mean_x = sum(x1_ndarray * x3_ndarray) / sum(x3_ndarray)
    sigma_x = np.sqrt(
        sum(x3_ndarray * (x1_ndarray - mean_x)**2) / sum(x3_ndarray))
    mean_y = sum(x2_ndarray * x3_ndarray) / sum(x3_ndarray)
    sigma_y = np.sqrt(
        sum(x3_ndarray * (x2_ndarray - mean_y)**2) / sum(x3_ndarray))

    # test data
    g = gaussian2D(x, y, mean_x, mean_y, sigma_x, sigma_y, 1.1)

    initial = Parameters()
    initial.add("height", value=max(x3_ndarray))
    initial.add("centroid_x", value=mean_x)
    initial.add("centroid_y", value=mean_y)
    initial.add("sigma_x", value=sigma_x)
    initial.add("sigma_y", value=sigma_y)
    initial.add("background", value=0.)

    fit = minimize(residuals, initial, args=(x, y, g))
    # print(type(fit))
    # print(type(report_fit(fit)))
    # print(fit)
    f = open(gauss_w_path, "w")
    f.write(str(fit.__dict__))
    # # showFig(x1_ndarray, x2_ndarray, x3_ndarray)


def main():
    process_data(joint_frequency_path1, w_twod_gauss_params_txt_path1)
    # process_data(joint_frequency_path2, w_twod_gauss_params_txt_path2)
    process_data(extend_selected_avg_parti_trimmed_dict_path,
                 w_extended_selected_avg_gauss_params_txt_path)

    f = open(w_extended_selected_avg_gauss_params_txt_path, "r")
    extended_result = f.read()
    Px = float(extended_result[extended_result.find(
        '\'centroid_x\':'):extended_result.find('\'centroid_y\':')].split(": ")[1].split(",")[0])
    Py = float(extended_result[extended_result.find(
        '\'centroid_y\':'):extended_result.find('\'sigma_x\':')].split(": ")[1].split(",")[0])
    # eDistance = math.dist([Px, Py], [Qx, Qy])
    # print(eDistance)

    f = open(w_twod_gauss_params_txt_path1, "r")
    population_result = f.read()
    Qx = float(population_result[population_result.find(
        '\'centroid_x\':'):population_result.find('\'centroid_y\':')].split(": ")[1] .split(",")[0])
    Qy = float(population_result[population_result.find(
        '\'centroid_y\':'):population_result.find('\'sigma_x\':')].split(": ")[1].split(",")[0])
    eDistance = math.dist([Px, Py], [Qx, Qy])

    extended_sigma_x = float(extended_result[extended_result.find(
        '\'sigma_x\':'):extended_result.find('\'sigma_y\':')].split(": ")[1].split(",")[0])
    extended_sigma_y = float(extended_result[extended_result.find(
        '\'sigma_y\':'):extended_result.find('\'background\':')].split(": ")[1].split(",")[0])
    extended_combined_sigma = math.sqrt(
        extended_sigma_x ** 2 + extended_sigma_y ** 2)

    population_sigma_x = float(population_result[population_result.find(
        '\'sigma_x\':'):population_result.find('\'sigma_y\':')].split(": ")[1].split(",")[0])
    population_sigma_y = float(population_result[population_result.find(
        '\'sigma_y\':'):population_result.find('\'background\':')].split(": ")[1].split(",")[0])
    population_combined_sigma = math.sqrt(
        population_sigma_x ** 2 + population_sigma_y ** 2)

    total_sigma = population_combined_sigma + extended_combined_sigma
    if total_sigma >= eDistance:
        print("Gauss Test Passed !")
        print("eDistance: ", eDistance, "total_sigma: ", total_sigma)


if __name__ == "__main__":
    main()
