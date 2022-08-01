import csv
with open('/root/KL_Divergence/user_gauss_params/data/combine/user_1_comnbined.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        print(row[0])