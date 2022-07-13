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
      Total_rawDataSize = int(4096)


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
          # if feaID == "4":
          #   print(d_mins)
          #   print(d_mins)
          #   print(d_weights)
          #   print(data[user_str])
          #   print(type(d_mins))
            # break
          for gid in range(no_gauss):
            # print(type(gidq))
            
            K_str = str(user_str+"_"+str(gid))
        
            user_Fea_g_dict[K_str]= tuple([float(d_mins[gid]), float(d_maxs[gid]), float(d_weights[gid]) ,float(0.0)])

      print("user_Fea_g_dict done")

      Bmax = max(Total_maxList)
      Bmin = min(Total_minList)
      sample_range = Bmax-Bmin
      step = sample_range/10
      left_point = Bmin
      num_eachrange = int(Total_rawDataSize/10)
      # print(num_eachrange)
      slice_counter = 0
      while left_point <= Bmax-step:
          right_point = left_point+step
          # print(slice_counter)
          slice_counter+=1
          rangeList = []
          for i in range(num_eachrange):
            # print(i)
            sam_point = random.uniform(left_point , right_point)
            rangeList.append(sam_point)
            for key, value in user_Fea_g_dict.items():
                vList = tuple(value)
                if vList[0] <= sam_point and sam_point >= vList[1]:
                  # print("here")
                  user_Fea_g_dict.update({key:tuple([vList[0], vList[1], vList[2], 1+vList[3]])})
      # min, max, weight, counts
      # vList[2] weight of the sub gauss under this user_fea json object
          left_point=right_point
          totalRange_List.append(rangeList)


      # multiple + plus

      for key, value in user_Fea_g_dict.items():
      
        theUserK=key[0:findNth(key,"_",2)]
        print(theUserK)
        if theUserK in Udict:
          Udict[theUserK] +=value[2]*value[3]
        else: 
          Udict[theUserK]=value[2]*value[3]

print(Udict)
f = open(true_datapath + \
          "united_gauss/0/0.json")
data = json.load(f)
total_size = 0
for key, value in data.items():
  total_size += int(value["raw_data_size"])
  
result_dict = {}  
for key, value in data.items():
  result_dict[key] = int(value["raw_data_size"]) / total_size


print(result_dict)

      # print(user_Fea_g_dict)