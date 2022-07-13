import pandas as pd
import os
subfolders = [x[0] for x in os.walk("/home/xphuang/entropy/user_gauss_params/data/nofeatures")]
for F in subfolders:
    gauss_users_dir = subf
    featureID = subf[subf.rfind("/")+1:len(subf)]
        users_list = json_under_this_dir(fea_dirs)
        for user_gauss_file in users_list: