import numpy as np
import matplotlib.pyplot as plt
from lmfit import Parameters, minimize, report_fit
from scipy.interpolate import griddata


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


file_data1 = []
nnz = []
aau = []
iil = []


def process_data():
    file_data1 = np.loadtxt(joint_frequency_path1,
                            delimiter=',', skiprows=1)
    # sg = []
    for col1, col2, col3 in file_data1:
        # sg.append([col1, col2])
        nnz.append(col1)
        aau.append(col2)
        iil.append(col3)


def printFig(x, y, z):
    X, Y = np.meshgrid(np.linspace(x.min(), x.max(), 1000),
                       np.linspace(y.min(), y.max(), 1000))

    Z = griddata((x, y), z, (X, Y), method='linear', fill_value=0)
    fig, ax = plt.subplots()
    art = ax.pcolor(X, Y, Z, shading='auto')
    plt.colorbar(art, ax=ax, label='z')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.show()


def main():
    process_data()
    nz = np.asarray(nnz, dtype=np.float32)
    au = np.asarray(aau, dtype=np.float32)
    il = np.asarray(iil, dtype=np.float32)
    x, y = np.meshgrid(np.linspace(nz.min(), nz.max(), 100),
                       np.linspace(au.min(), au.max(), 100))

    arr = np.stack((nz, au), axis=1)
    print(type(arr))
    # weighted arithmetic mean (corrected - check the section below)
    mean_x = sum(nz * il) / sum(il)
    sigma_x = np.sqrt(sum(il * (nz - mean_x)**2) / sum(il))
    mean_y = sum(au * il) / sum(il)
    sigma_y = np.sqrt(sum(il * (au - mean_y)**2) / sum(il))
    print(mean_x)
    print(mean_y)

    # test data
    g = gaussian2D(x, y, mean_x, mean_y, sigma_x, sigma_y, 1.1)

    initial = Parameters()
    initial.add("height", value=max(il))
    initial.add("centroid_x", value=mean_x)
    initial.add("centroid_y", value=mean_y)
    initial.add("sigma_x", value=sigma_x)
    initial.add("sigma_y", value=sigma_y)
    initial.add("background", value=0.)

    fit = minimize(residuals, initial, args=(x, y, g))
    print(report_fit(fit))
    printFig(nz, au, il)


if __name__ == "__main__":
    main()
