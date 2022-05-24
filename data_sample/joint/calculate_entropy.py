import json
import pandas as pd
from scipy.integrate import quad
import numpy as np

w_user1_params_json = 'user1_params.json'

def gauss(x, mu, sigma, A):
    return A*np.exp(-(x-mu)**2/2/sigma**2)


def multi_bimodal(x, *params):
    print("*params", params)
    print("type(*params)", type(params))
    gausses = 0
    # print("gauss_index", gauss_index)
    paramssss = params
    # print("paramssss", paramssss)
    print("[0][0:3]",*params[0])
    index = 0
    gauss_index = int(len(*params)/3)
    for i in range(gauss_index):
        print("i::",i)
        gausses += gauss(x, *params[0][0+index*3:3+index*3])
        index += 1
    # if gauss_index == 5:

    return gausses


def integrand(x, a, b):
    return a*x**2 + b

def main():
  # a = 2
  # b = 1
  # I = quad(integrand, 15, 50,  args=(a,b))  
  # for loop all json

  f = open('user1_params.json')
  data = json.load(f)
  print("data x1",*(data["user1"]["0"]["x1"]))
  min = 15
  max = 50
  I = quad(multi_bimodal, 15, 50,  args=(data["user1"]["0"]["x1"]))  
  print("I:",I)
  # I = quad(gauss, 15, 50,  args=(3519.90196755, 3306.92316145, 9.99266278))    
  # print("I:",I)

  # for g in range(1000):
  #   x_for_sim = float(decimal.Decimal(random.randrange(int(min*100), int(max*100)))/100)
  #   y_for_sim = multi_bimodal(x_for_sim, *,data["user1"]["0"]["x1"])

  # for g in range(len(x1_list)):
  #     x_for_sim = float(decimal.Decimal(random.randrange(
  #         int(min(x1_list)*100), int(max(x1_list)*100)))/100)
  #     y_for_sim = multi_bimodal(
  #         x_for_sim, *params)
  #     ys_for_sim.append(y_for_sim)
  # return fit(z_list, ys_for_sim)




if __name__ == "__main__":
    main()
