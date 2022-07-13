import json
import random
from functools import reduce
# generate random samples
def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)


true_datapath = "/home/xphuang/entropy/user_gauss_params/data/"
featureGauss_list = ["0"]
Udict = {}
for ifeaID in range(4096):
      print(ifeaID)
      feaID=str(ifeaID)
      r_united_params_json = true_datapath + \
          "united_gauss/"+feaID+"/"+feaID+".json"
      w_consolidated_percent_json = true_datapath + \
          "entropy/entropysum_percent_"+feaID+".json"
      f = open(r_united_params_json)
      data = json.load(f)

      Total_maxList=[]
      Total_minList=[]
      Total_rawDataSize = int(4096/10)


      user_Fea_g_dict = {}
      totalRange_List = []


      for user_str in data.keys():
          # print("user_key", user_str)
          users_individual_gauss_entropy = []
          # this_d_data = data[user_str]["gauss"]
          # print("F35555", this_d_data)
          no_gauss = len(data[user_str]["min"])
          d_mins = data[user_str]["min"]
          d_maxs = data[user_str]["max"]
          d_weights = data[user_str]["weights"]
          d_uf_size = data[user_str]["raw_data_size"]
          Total_minList += d_mins
          Total_maxList += d_maxs
          # Total_rawDataSize += int(data[user_str]["raw_data_size"])
          # print(no_gauss)
          for gid in range(no_gauss):
            # print(type(gidq))
            
            K_str = str(user_str+"_"+str(gid))
            if feaID == 4:
              print(d_mins)
              print(d_mins)
              print(type(d_mins))
              


print(Udict)
      # print(user_Fea_g_dict)