import csv
import sys
csv.field_size_limit(sys.maxsize)
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

username = "user_1"
for key, value in dicts.items():
  with open('/root/KL_Divergence/user_gauss_params/data/nofeatures/'+username+"/"+username+"_"+str(key)+'_q.csv', 'w') as csvfile:
    print("nf_no:"+key)
    writer = csv.writer(csvfile)
    writer.writerow(row)
    # csvfile.writerow(value)
    

