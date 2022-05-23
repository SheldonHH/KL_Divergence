import pylab as plb
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
import json
from statistics import mean
import math
# x = ar(range(10))
# y = ar([0,1,2,3,4,5,4,3,2,1])
def Average(lst):
    return mean(lst)
def variance(data):
     # Number of observations
     n = len(data)
     # Mean of the data
     mean = sum(data) / n
     # Square deviations
     deviations = [(x - mean) ** 2 for x in data]
     # Variance
     variance = sum(deviations) / n
     return variance
def stdev(data):
     var = variance(data)
     std_dev = math.sqrt(var)
     return std_dev
def gaus(x, mu, sigma, A):
    return A*np.exp(-(x-mu)**2/2/sigma**2)

def write_dict_to_json(dict, json_to_write):
    df_params = pd.DataFrame.from_dict(dict)
    result = df_params.to_json(orient="columns")
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))

with open("sg.csv") as json_file:
    df = pd.read_csv("sg.csv", header=None)

sorted_df = df.sort_values(by=0)
# print(df)
x = list(sorted_df[0])
# kdd=pd.Series(x)
# kdd.sort_values(ascending=True)
# x.sort()
print(x)
y = list(sorted_df[1])
print(y)

n = len(sorted_df[0])                          #the number of data
# mean = sum(df[0]*df[1])/n                   #note this correction
mean = Average(x)
print("mean",mean)
# sigma = sum(df[1]*(df[0]-mean)**2)/n        #note this correction
sigma = stdev(df[0])
print("sigma",sigma)
peak = max(df[1])
print("peak",peak)
# def gaus(x,x0,sigma,a):
#     return a*np.exp(-(x-x0)**2/(2*sigma**2))


popt,pcov = curve_fit(gaus,x,y,p0=[mean,sigma,peak], maxfev=500000)
print(popt)
write_dict_to_json({"sg":popt},"ftw.json")

plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaus(x,*popt),'ro:',label='fit')
plt.legend()
plt.title('Fig. 3 - Fit for Time Constant')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.show()
