import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

x_frequency_path1 = 'data_sample/independent/x_frequency_user_1_data.csv'
joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'

file_data1 = np.loadtxt(x_frequency_path1,
                        delimiter=',')

sg = []
il = []
print(type(file_data1))
# file_data1.sort(axis=1)

sorted_data = file_data1[file_data1[:, 0].argsort()]
for col1, col2 in sorted_data:
    sg.append(col1)
    il.append(col2)
npa = np.asarray(sg, dtype=np.float32)
npb = np.asarray(il, dtype=np.float32)
x = npa
y = npb

# weighted arithmetic mean (corrected - check the section below)
mean = sum(x * y) / sum(y)
sigma = np.sqrt(sum(y * (x - mean)**2) / sum(y))


def Gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))


popt, pcov = curve_fit(Gauss, x, y, p0=[max(y), mean, sigma], maxfev=500000)

plt.plot(x, y, 'b+:', label='data')
plt.plot(x, Gauss(x, *popt), 'r-', label='fit')
plt.legend()
plt.title('Fig. 3 - Fit for Time Constant')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.show()
