import json
import random
import pandas as pd
# generate random samples
def write_dict_to_json(dict, json_to_write):
    df_params = pd.DataFrame.from_dict({k: [v] for k, v in dict.items(
    )}, orient="index", columns=["user profit percentage"])
    result = df_params.to_json()
    parsed = json.loads(result)
    with open(json_to_write, 'w') as convert_file:
        convert_file.write(json.dumps(parsed))


def main():
  true_datapath = "/home/xphuang/entropy/user_gauss_params/data/"
  # featureGauss_list = ["0"]
  Udict = {}
  for intfeaID in range(4096):
    feaID = str(intfeaID)
    print("feaID",feaID)
    r_united_params_json = true_datapath + \
      "united_gauss/"+feaID+"/"+feaID+".json"
    w_consolidated_percent_json = true_datapath + \
      "entropy/entropysum_percent_"+feaID+".json"
    f = open(r_united_params_json)
    data = json.load(f)
    cal_percent(r_united_params_json, w_consolidated_percent_json, data,Udict)
  
  write_dict_to_json(Udict,w_consolidated_percent_json)

def cal_percent(r_united_params_json,w_consolidated_percent_json,data,Udict):
  Total_maxList=[]
  Total_minList=[]
  Total_rawDataSize = 0
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
    Total_rawDataSize += int(data[user_str]["raw_data_size"])
    for gaussId in range(no_gauss):
      user_Fea_g_dict[user_str+"_"+str(gaussId)]= tuple([float(d_mins[gaussId]), float(d_maxs[gaussId]), float(d_weights[gaussId]) ,float(0)])



  Bmax = max(Total_maxList)
  Bmin = min(Total_minList)
  sample_range = Bmax-Bmin
  step = sample_range/10
  left_point = Bmin
  num_eachrange = int(Total_rawDataSize/10)
  right_point = 0
  slice_counter = 0
  while left_point <= Bmax-step:
    # print(slice_counter)
    slice_counter+=1
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
  # vList[2] weight of the sub gauss under this user_fea json object
    left_point=right_point
    totalRange_List.append(rangeList)
    # multiple + plus
    countss = 0
    for key, value in user_Fea_g_dict.items():
      print(countss)
      countss+=1
      # print(key[0:key.rfind("_")])
      theUserK=key[0:key.rfind("_")]
      if theUserK in Udict:
        Udict[theUserK] +=value[2]*value[3]
      else: 
        Udict[theUserK]=value[2]*value[3]

  # print(user_Fea_g_dict)

if __name__ == "__main__":
    main()