import csv
import sys
import pandas as pd
csv.field_size_limit(sys.maxsize)

# write to dicts
with open('/root/KL_Divergence/user_gauss_params/data/combine/user_1_comnbined.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',')
  counter = 0
  dicts = {}
  for row in spamreader:
    print(counter)
    for i in range(len(row)):
      if i in dicts:
        existedList = list(dicts[i])
        newList =existedList.append(row[i])
        dicts[i] = existedList
      else:
        dicts[i]=[row[i]]
    counter+=1


# dicts{} to csv
username = "user_1"
for key, value in dicts.items():
    target_nf_path = '/root/KL_Divergence/user_gauss_params/data/nofeatures/'+username+"/"+username+"_"+str(key)+'_onerow.csv'
    with open(target_nf_path, 'w') as csvfile:
      print("nf_no:",key)
      writer = csv.writer(csvfile)
      writer.writerow(value)
      # for item in value:
      #   writer.writerow(item)

    # transpose the file
    # pd.read_csv(target_nf_path, delimiter=" ").T.to_csv(target_nf_path, header=False, index=False)
    # csvfile.writerow(value)
    

