Input:  raw data (userx_data)
Output: gauss params for each dimension of the user's data

Required File Format:
`user_x.csv`

### Required Directory Structure:
```
data 
│   user_x.csv (raw data)
└───features
│   └───freq 
│       │ 
```

## Installation 
```
cd py
pip3 isntall -r requirements.txt
```

### Generate Gaussian Parameters for a typical individual user
```
go run main.go
```

#### Developer Notes
Intermediated Files except raw data and final result
```
data 
│   user_x.csv (raw data)
|   user_x.jpeg 
└───features
│   │   user_x_feature.csv
│   └───freq
│       │   user_x_freq.csv
│       │   user_x_features_gauss.json (final result)
``` 


1. preprocess each dimension of user's data to dense_trimmed_user_x_data.csv 
2. generate the frequence data for each dimension of the user's data
3. generate gauss params for each dimension of the user's data


```
go mod init userGenerateGauss
```