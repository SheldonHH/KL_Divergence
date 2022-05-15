import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

import lmfit
from lmfit.lineshapes import gaussian2d, lorentzian


joint_frequency_path1 = 'data_sample/joint/joint_frequency_1.csv'
joint_frequency_path2 = 'data_sample/joint/joint_frequency_2.csv'

sg = []
il = []
au = []
file_data1 = np.loadtxt(joint_frequency_path1,
                        delimiter=',', skiprows=1)
x_sorted_data = file_data1[file_data1[:, 0].argsort()]
print(x_sorted_data)
y_sorted_data = file_data1[file_data1[:, 1].argsort()]
print(y_sorted_data)

for col1, col2, col3 in file_data1:
    sg.append(col1)
    il.append(col2)
    au.append(col3)
npa = np.asarray(sg, dtype=np.float32)
print(npa)
npb = np.asarray(il, dtype=np.float32)
npc = np.asarray(au, dtype=np.float32)
x = npa
y = npb
z = npc


# npoints = 10000
# np.random.seed(2021)
# x = np.random.rand(npoints)*10 - 4
# y = np.random.rand(npoints)*5 - 3
# z = gaussian2d(x, y, amplitude=30, centerx=2,
#                centery=-.5, sigmax=.6, sigmay=.8)
# z += 2*(np.random.rand(*z.shape)-.5)
error = np.sqrt(z+1)
print(x.max())
X, Y = np.meshgrid(np.linspace(x.min(), x.max(), 1000),
                   np.linspace(y.min(), y.max(), 1000))
Z = griddata((x, y), z, (X, Y), method='linear', fill_value=0)

model = lmfit.models.Gaussian2dModel()
params = model.guess(z, x, y)
print(params)
result = model.fit(z, x=x, y=y, params=params, weights=1)
lmfit.report_fit(result)
print(lmfit.report_fit(result))


fig, ax = plt.subplots()
art = ax.pcolor(X, Y, Z, shading='auto')
plt.colorbar(art, ax=ax, label='z')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()
