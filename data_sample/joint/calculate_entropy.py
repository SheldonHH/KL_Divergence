import json
import pandas as pd
from scipy.integrate import quad

w_user1_params_json = 'user1_params.json'

def integrand(x, a, b):
    return a*x**2 + b

def gauss(x, mu, sigma, A):
    return A*exp(-(x-mu)**2/2/sigma**2)


def multi_bimodal(x, *params):
    gausses = 0
    # print("gauss_index", gauss_index)
    paramssss = params
    # print("paramssss", paramssss)
    index = 0
    for i in range(gauss_index):
        gausses += gauss(x, *params[0+index*3:3+index*3])
        index += 1
    return gausses

def main():
  a = 2
  b = 1
  I = quad(integrand, 15, 50,  args=(a,b))
      ys_for_sim = []
    for g in range(len(x1_list)):
        x_for_sim = float(decimal.Decimal(random.randrange(
            int(min(x1_list)*100), int(max(x1_list)*100)))/100)
        y_for_sim = multi_bimodal(
            x_for_sim, *params)
        ys_for_sim.append(y_for_sim)
    return fit(z_list, ys_for_sim)




if __name__ == "__main__":
    main()
