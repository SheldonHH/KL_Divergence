import numpy as np
# from sklearn.mixture import GaussianMixture
# https://stackoverflow.com/a/35992526/5772735
from curses import raw
from ntpath import join
from re import S
from pylab import *
from scipy import linalg
from scipy.optimize import curve_fit
from scipy.stats import entropy
from scipy.stats import norm
from sklearn import mixture
import numpy as np
import pandas as pd
import json
import random
import decimal
from scipy.interpolate import UnivariateSpline
import itertools
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl


# Creating a Function.
def simulated_height_normal_dist(x, mean, sd):
    # prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
    # return prob_density
    # print(norm.cdf(x, mean, sd))
    return norm.cdf(x, mean, sd)

def write_dict_to_json(dict, json_to_write):
    df_params = pd.DataFrame.from_dict(dict)
    result = df_params.to_json(orient="columns")
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))

def calculate_MSE(z_list, ys_for_sim):
    y = z_list
    y_bar = ys_for_sim
    # print("z_list", z_list)
    # print("y_bar", y_bar)
    summation = 0  # variable to store the summation of differences
    n = len(y)  # finding total number of items in list
    for i in range(0, n):  # looping through each element of the list
        # finding the difference between observed and predicted value
        difference = y[i] - y_bar[i]
        squared_difference = difference**2  # taking square of the differene
        # taking a sum of all the differences
        summation = summation + squared_difference
    MSE = summation/n  # dividing summation by total values to obtain average
    # print("The Mean Square Error is: ", MSE)
    return MSE

def obtain_first_second(x, y, strtype):
    dy=np.diff(x,1)
    dx=np.diff(y,1)
    yfirst=dy/dx
    xfirst=0.5*(x[:-1]+x[1:])
    dyfirst=np.diff(yfirst,1)
    dxfirst=np.diff(xfirst,1)
    
    if(strtype == "second"):
        ysecond=dyfirst/dxfirst
        xsecond=0.5*(xfirst[:-1]+xfirst[1:])
        return ysecond
    else:
        return yfirst

def gauss(x, mu, sigma, A):
    return A*exp(-(x-mu)**2/2/sigma**2)


def multi_bimodal(x, weights_array, *params):
    gauss_index = int(len(params)/3)
    gausses = 0
    for i in range(gauss_index):
        gausses += weights_array[i]*gauss(x, *params[0+i*3:3+i*3])
    return gausses


def read_from_csv(r_dense_trimmed_data_path1, before_extension_half, first_half):
    df = pd.read_csv(r_dense_trimmed_data_path1)
    return write_to_json(df, before_extension_half, first_half)


def write_to_json(df, before_extension_half, first_half):
    w_freq_path = first_half + \
        "independent/freq_"+before_extension_half+".json"
    w_percent_freq_path = first_half + \
        "independent/percent_freq_"+before_extension_half+".json"
    freq_json_file_to_write = open(w_freq_path, 'w')
    percent_freq_json_file_to_write = open(w_percent_freq_path, 'w')
    # json_file_to_write.write(json.dumps(df['x1'].value_counts().to_dict()))
    trimmed_dict = df.to_dict()
    freq_dict = {}

    count_dict = {}
    for key, value in trimmed_dict.items():
        freq_dict[key] = pd.DataFrame.from_dict(
            value, orient='index').value_counts().to_dict()
        # print("len", len(freq_dict[key]))
        count_dict[key] = len(freq_dict[key])

    final_col_percentFreq_dict = {}
    final_col_freq_dict = {}
    for bigger_key, bigger_value in freq_dict.items():
        col_freq_dict = {}
        col_percentFreq_dict = {}
        for key, value in bigger_value.items():
            col_freq_dict[key[0]] = value
            col_percentFreq_dict[key[0]] = value / count_dict[bigger_key]
        final_col_freq_dict[bigger_key] = col_freq_dict
        final_col_percentFreq_dict[bigger_key] = col_percentFreq_dict
    freq_json_file_to_write.write(json.dumps(final_col_freq_dict))
    percent_freq_json_file_to_write.write(
        json.dumps(final_col_percentFreq_dict))
    return final_col_percentFreq_dict
    # with open(w_freq_path, 'r') as f:
    #     freq_dict = json.load(f)
    # with open(w_percent_freq_path, 'r') as f:
    #     freq_dict = json.load(f)


def plot_results(X, Y, means, covariances, index, title):
    splot = plt.subplot(5, 1, 1 + index)
    for i, (mean, covar, color) in enumerate(zip(means, covariances, color_iter)):
        v, w = linalg.eigh(covar)
        v = 2.0 * np.sqrt(2.0) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])
        # as the DP will not use every component it has access to
        # unless it needs it, we shouldn't plot the redundant
        # components.
        if not np.any(Y == i):
            continue
        plt.scatter(X[Y == i, 0], X[Y == i, 1], 0.8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan(u[1] / u[0])
        angle = 180.0 * angle / np.pi  # convert to degrees
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180.0 + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        splot.add_artist(ell)

    plt.xlim(-6.0, 4.0 * np.pi - 6.0)
    plt.ylim(-5.0, 5.0)
    plt.title(title)
    plt.xticks(())
    plt.yticks(())

#  The four initializations are
#  kmeans (default), random, random_from_data and k-means++.
#  eventual associated classification after GMM has finished


def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros


def main():
    args = sys.argv[1:]
    # print(args)
    # user_1_data
    raw_data_path1 = args[0]
    middle_index = args[0].rindex('/')
    last_index = len(args[0])-1
    first_half = args[0][0:middle_index+1]
    before_extension_half = args[0][middle_index+1: args[0].rindex('.')]
    w_the_user_params_json = first_half+'gauss_result/' + \
        before_extension_half+'_params.json'


    r_dense_trimmed_data_path1 = first_half + \
        "trimmed/dense_trimmed_"+before_extension_half+".csv"
    final_col_percentFreq_dict = read_from_csv(
        r_dense_trimmed_data_path1, before_extension_half, first_half)

    # Parameters
    n_samples = 100

    # Generate random sample following a sine curve
    np.random.seed(0)
    X = np.zeros((n_samples, 2))

    i = 0
    dimension_min_with_params = []
    less_1, equal_1, larger_1 = 0,0,0
    for key, value in final_col_percentFreq_dict.items():
        min_index = 0
        n_samples = len(list(value.keys()))
        X = np.zeros((n_samples, 2))
        # for each dimension
        if len(value.keys())<1:
            dimension_min_with_params.append({key+"_gauss": [0],"max":0, "min":0})
            less_than_1 += 1
        if len(value.keys())==1:
            equal_1 += 1
            dimension_min_with_params.append({key+"_gauss": X[0][0],"max":max(X[:,0]),"min":min(X[:,0])})
        if len(value.keys()) >1:
            larger_1 +=1
            for i in range(len(list(value.keys()))):
                X[i, 0] = list(value.keys())[i]
                X[i, 1] = list(value.values())[i]
                i += 1
            # print("X[,]",X[:,1])
        
            num_with_params = {}
            # one to ten Gauss
            counter_initial=10
            MSE_list, ySp, xSp = [],[],[]
            y_firsts, y_seconds = [],[]
            for index in range(counter_initial):
                if n_samples < index+1:
                    # dimension_min_with_params.append({key+"_gauss": num_with_params[min_index],"max":max(X[:,0]),"min":min(X[:,0])})
                    break
                gmm = mixture.GaussianMixture(n_components=index+1, covariance_type="diag", max_iter=500000).fit(X)
                list_params = zerolistmaker((index+1)*3)
                params = tuple(list_params)
                # print("index", index)
                # print("gmm.means_", gmm.means_[index][0])
                simulated_y_sum = 0
                for sub_index in range(index+1):
                    list_params[sub_index*3] = gmm.means_[sub_index][0]
                    list_params[sub_index*3+1] = gmm.covariances_[sub_index][0]
                    list_params[sub_index*3+2] = simulated_height_normal_dist(gmm.means_[sub_index][0], gmm.means_[sub_index][0], math.sqrt(gmm.covariances_[sub_index][0]))*gmm.weights_[sub_index]
                    # print("simulated_height_normal_dist",list_params[sub_index*3+2]*gmm.weights_[sub_index])
                    simulated_y_sum += list_params[sub_index*3+2]*gmm.weights_[sub_index]
            
                params = tuple(list_params)
                num_with_params[index] = list_params
                # Calculate the MSE for each Gauss
                ys_for_sim = [] # different from assign the value 
                for g in range(X[:,0].size):
                    x_for_sim = X[g][0]
                    y_for_sim = multi_bimodal(
                        x_for_sim, gmm.weights_ , *params)
                    ys_for_sim.append(y_for_sim)
                MSE = calculate_MSE(X[:,1].tolist(), ys_for_sim)
                ySp.append(MSE)
                xSp.append(index)
                MSE_list.append(MSE)
            incre_index = counter_initial

            while(True):
                if n_samples < incre_index+1:
                    # dimension_min_with_params.append({key+"_gauss": num_with_params[min_index],"max":max(X[:,0]),"min":min(X[:,0])})
                    break
                gmm = mixture.GaussianMixture(n_components=incre_index+1, covariance_type="diag", max_iter=100).fit(X)
                list_params = zerolistmaker((incre_index+1)*3)
                params = tuple(list_params)
                simulated_y_sum = 0
                for sub_index in range(incre_index+1):
                    list_params[sub_index*3] = gmm.means_[sub_index][0]
                    list_params[sub_index*3+1] = gmm.covariances_[sub_index][0]
                    list_params[sub_index*3+2] = simulated_height_normal_dist(gmm.means_[sub_index][0], gmm.means_[sub_index][0], math.sqrt(gmm.covariances_[sub_index][0]))*gmm.weights_[sub_index]
                    # print("simulated_height_normal_dist",list_params[sub_index*3+2]*gmm.weights_[sub_index])
                    simulated_y_sum += list_params[sub_index*3+2]*gmm.weights_[sub_index]
                params = tuple(list_params)
                num_with_params[incre_index] = list_params
                # print(str(index+1),params,len(params))
                # Calculate the MSE for each Gauss
                ys_for_sim = [] # different from assign the value 
                for g in range(X[:,0].size):
                    x_for_sim = X[g][0]
                    y_for_sim = multi_bimodal(
                        x_for_sim, gmm.weights_ , *params)
                    ys_for_sim.append(y_for_sim)
                MSE = calculate_MSE(X[:,1].tolist(), ys_for_sim)
                MSE_list.append(MSE)
                
                # print(MSE_list)
                # print("-----------------------------")
                ySp.append(MSE)
                xSp.append(incre_index)


                y_firsts = obtain_first_second(np.array(ySp),np.array(xSp),"first")
                y_seconds = obtain_first_second(np.array(ySp),np.array(xSp),"second")
                if(abs(y_seconds[-1]) < 0.1 or y_firsts[-1]>0 or incre_index==100):
                    print("incre_index", incre_index)
                    print("global_params", params)
                    print("ySp", ySp)
                    print("ySp.index(min(ySp))", ySp.index(min(ySp)))
                    min_index = ySp.index(min(ySp))
                    print("xSp",xSp)
                    # print("x_range",x_range)
                    y_firsts = obtain_first_second(np.array(ySp),np.array(xSp),"first")
                    y_seconds = obtain_first_second(np.array(ySp),np.array(xSp),"second")

                    print("y_seconds",y_seconds)
                    print("y_firsts",y_firsts)
                    super_global_params = params
                    break
                incre_index += 1
            print(key," result:", num_with_params[min_index])
            dimension_min_with_params.append({key+"_gauss": num_with_params[min_index],"max":max(X[:,0]),"min":min(X[:,0])})
    print("less_1",less_1,"equal_1",equal_1,"larger_1",larger_1)
    write_dict_to_json({"user1": dimension_min_with_params}, w_the_user_params_json)     
   
        # ys_for_sim.append(y_for_sim)
            # print("gmm.weights_", gmm.weights_)
            # print("gmm.covariances_", gmm.covariances_)
            # print("gmm.precisions_cholesky_", gmm.precisions_cholesky_)
            # print("sum(gmm.weights_)", sum(gmm.weights_))
            # print("gmm.means_", gmm.means_)
            #
            #
            # for sub_index in range(index+1):
            #     print("sub_index", sub_index)
            # params[sub_index*3] = gmm.means_[sub_index]
            #     params[sub_index*3+1] = gmm.covariances_array[sub_index][0]
            #     params[sub_index*3+2] = simulated_height_normal_dist(
            #         gmm.means_[sub_index], gmm.means_[sub_index], gmm.covariances_array[sub_index][0])
            #     # calculate the MSE for each Gauss number of test
            # ys_for_sim = []
            # for g in range(len(X[i, 0])):
            #     x_for_sim = float(decimal.Decimal(random.randrange(
            #         int(min(X[i, 0])*100), int(max(X[i, 0])*100)))/100)
            #     y_for_sim = multi_bimodal(
            #         x_for_sim, *params)
            #     ys_for_sim.append(y_for_sim)
        # print("gmm.weights_", gmm.weights_)
        # print("gmm.covariances_", gmm.covariances_)
        # print("gmm.precisions_cholesky_", gmm.precisions_cholesky_)
        # print("sum(gmm.weights_)", sum(gmm.weights_))
        # print("gmm.means_", gmm.means_)
    # plt.figure(figsize=(10, 10))
    # plt.subplots_adjust(
    #     bottom=0.04, top=0.95, hspace=0.2, wspace=0.05, left=0.03, right=0.97
    # )
    # Fit a Gaussian mixture with EM using ten components

    # plot_results(
    #     X, gmm.predict(X), gmm.means_, gmm.covariances_, 0, "Expectation-maximization"
    # )


if __name__ == "__main__":

    main()
