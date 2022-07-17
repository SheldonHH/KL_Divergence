for VARIABLE in 0 1 2 3 4 5 .. N
    awk -F "\"*,\"*" '{print $VARIABLE}' /home/xphuang/entropy/user_gauss_params/data/combine/user_2_comnbined.csv
