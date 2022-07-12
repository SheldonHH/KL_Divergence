import json
import random
# generate random samples

true_datapath = "/root/KL_Divergence/user_gauss_params/data/"
featureGauss_list = ["0"]
for feaID in featureGauss_list:
  r_united_params_json = true_datapath + \
      "united_gauss/"+feaID+"/"+feaID+".json"
  w_consolidated_percent_json = true_datapath + \
      "entropy/entropysum_percent_"+feaID+".json"
f = open(r_united_params_json)
data = json.load(f)

Total_maxList=[]
Total_minList=[]
Total_rawDataSize = 0


user_Fea_g_dict = {}
totalRange_List = []



for user_str in data.keys():
    print("user_key", user_str)
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
    Total_rawDataSize += int(data[user_str]["raw_data_size"])
    for gaussId in range(no_gauss):
      user_Fea_g_dict[user_str+"_"+str(gaussId)]= tuple([float(d_mins[gaussId]), float(d_maxs[gaussId]), float(d_weights[gaussId])*float(d_uf_size) ,float(0)])



max = max(Total_maxList)
min = min(Total_minList)
sample_range = max-min
step = sample_range/10
left_point = min
num_eachrange = int(Total_rawDataSize/10)
right_point = 0
while left_point < max-step:
  right_point += left_point+step
  rangeList = []
  for i in range(num_eachrange):
    sam_point = random.uniform(left_point , right_point)
    rangeList.append(sam_point)
    for key, value in user_Fea_g_dict.items():
        vList = tuple(value)
        if vList[0] < sam_point and sam_point > vList[1]:
          user_Fea_g_dict.update({key:tuple([vList[0], vList[1], vList[2], 1+vList[3]])})
# min, max, weight, counts

  left_point=right_point
  totalRange_List.append(rangeList)



  print(user_Fea_g_dict)