import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy import savetxt
import pickle

# You'll obviously need to reshape the output for plotting, e.g:

joint_frequency_path1 = 'data_sample/joint/joint_frequency_1.csv'
joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'


def twoD_Gaussian(point, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp(- (a*((point[0]-xo)**2) + 2*b*(point[0]-xo)*(point[1]-yo)
                                     + c*((point[1]-yo)**2)))
    return g.ravel()


file_data1 = []


def read_data_from_csv():
    file_data1 = np.loadtxt(joint_frequency_path1,
                            delimiter=',', skiprows=1)


def main():
    file_data1 = np.loadtxt(joint_frequency_path1,
                            delimiter=',', skiprows=1)
    sg = []
    il = []

    for col1, col2, col3 in file_data1:
        sg.append([col1, col2])
        il.append([col3])
    npa = np.asarray(sg, dtype=np.float32)
    npb = np.asarray(il, dtype=np.float32)

    x = np.linspace(0, 200, 201)
    y = np.linspace(0, 200, 201)
    x, y = np.meshgrid(x, y)
    arr = np.stack((x, y), axis=1)
    print(arr)
    # output = open('test.pkl', 'wb')
    # pickle.dump(arr, output)
    # output.close()
    data = twoD_Gaussian(arr, 3, 100, 100, 20, 40, 0, 10)

# print(data)
# plot twoD_Gaussian data generated above
# plt.figure()
# c = plt.imshow(npa.reshape(16, 73))
# # plt.imshow(np.dstack([data.reshape(22, 22)]*3))
# plt.colorbar(c)
# plt.show()
# Do the fitting as before:


# add some noise to the data and try to fit the data generated beforehand
    initial_guess = (3, 100, 100, 20, 40, 0, 10)

    data_noisy = data + 0.2*np.random.normal(size=data.shape)
    # print(data_noisy)

    popt, pcov = curve_fit(twoD_Gaussian, data, data_noisy, p0=initial_guess)
    # print(data_noisy)
    # print(type(data_noisy))
    # And plot the results:
    # print(popt)

    data_fitted = twoD_Gaussian(arr, *popt)


if __name__ == "__main__":

    main()
