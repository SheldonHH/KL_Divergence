import pandas as pd
import time
import pandas as pd
import os

def create_q(Inputdicts):
    # t0 = time.time()
    # df = pd.read_csv("/home/xphuang/entropy/user_gauss_params/data/individual_features/user_2_comnbined.csv", delimiter=" ")
    # t1 = time.time()
    # print("#0: readcsv time:",t1-t0)

    t0 = time.time()
    for idx in range(4096): 
      df = pd.read_csv("/home/xphuang/entropy/user_gauss_params/data/individual_features/T/transposed_"+str(idx)+".csv", delimiter=",")
      for userkey, value in Inputdicts.items():
          print("userkey",userkey)
          each_fea = []
          uq_path = "/home/xphuang/entropy/user_gauss_params/data/q/"+userkey+"/"
          if os.path.isdir(uq_path) == False:
              os.mkdir(uq_path)
              data4=df.iloc[value[0]:value[1],idx]
            #   data4.to_csv("/home/xphuang/entropy/user_gauss_params/data/individual/feature_"+userkey+"_"+str(idx)+".csv", header=False,index=False)

              vcd4=(data4.value_counts(normalize=True))
            #   vcd4.to_csv(uq_path+userkey+"_"+str(idx)+"_new_q.csv", header=False)
              each_fea.append(vcd4)
    t1 = time.time()
    print("1-200 rows, 4096 Individual time:",t1-t0)

    # t0 = time.time()
    # key = "user_98"
    # df_col = pd.concat(each_fea)
    # df_col.to_csv("/home/xphuang/KL_Divergence/user_gauss_params/data/combine/" +
    #                 key+"_freq.csv", header=False, index=False)
    # # print(data4)
    # t1 = time.time()
    # print("iloc time:",t1-t0)



def main():
    Inputdicts = {"user_1": [1, 10000], "user_2": [10000, 20000], "user_3": [20000, 30000], "user_4": [30000,40000], "user_5": [40000,50000], "user_6": [50000,60000]}
    t0 = time.time()
    create_q(Inputdicts)
    t1 = time.time()
    print("create Q process time:",t1-t0)


if __name__ == "__main__":
    main()
