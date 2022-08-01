import pandas as pd
import time
import pandas as pd
import os
from H_qf_to_g_6 import *
from M_United import *

def create_q(Inputdicts):
    t0 = time.time()
    df = pd.read_csv("/home/xphuang/entropy/user_gauss_params/data/combine/user_2_comnbined.csv", delimiter=" ")
    t1 = time.time()
    print("readcsv time:",t1-t0)
    # dfRange = df.iloc[start:end]
    # value:[]


    # df.head(199).to_csv("/home/xphuang/entropy/user_gauss_params/data/combine/small_q.csv", header=False,index=False)

    t0 = time.time()
    for userkey, value in Inputdicts.items():
        each_fea = []
        uq_path = "/home/xphuang/entropy/user_gauss_params/data/q/"+userkey+"/"
        if os.path.isdir(uq_path) == False:
            os.mkdir(uq_path)
        for idx in range(4096): 
            print(idx)
            data4=df.iloc[value[0]:value[1],idx]
            data4.to_csv("/home/xphuang/entropy/user_gauss_params/data/combine/"+userkey+"_combine.csv", header=False,index=False)
            # LDL = data4.to_numpy()
            # print(LDL)
            # print("data4", len(LDL))
            vcd4=(data4.value_counts(normalize=True))
            vcd4.to_csv(uq_path+userkey+"_"+str(idx)+"_q.csv", header=False)
            each_fea.append(vcd4)
    t1 = time.time()
    print("1-200 rows, 4096 Individual time:",t1-t0)

    t0 = time.time()
    key = "user_98"
    df_col = pd.concat(each_fea)
    df_col.to_csv("/home/xphuang/KL_Divergence/user_gauss_params/data/combine/" +
                    key+"_freq.csv", header=False, index=False)
    # print(data4)
    t1 = time.time()
    print("iloc time:",t1-t0)



def main():
    Inputdicts = {"user_1": [1, 10000], "user_2": [10000, 20000], "user_3": [20000, 30000], "user_4": [30000,40000], "user_5": [40000,50000], "user_6": [50000,60000]}

    create_q(Inputdicts)

    Dir = "/home/xphuang/entropy/user_gauss_params/data/"

    t0 = time.time()
    for key in Inputdicts.keys():
        f_to_g(Dir, key)
    t1 = time.time()
    print("gauss process time:",t1-t0)

    t0 = time.time()
    unit_gauss(Inputdicts.keys())
    t1 = time.time()
    print("gauss united process time:",t1-t0)


if __name__ == "__main__":
    main()
