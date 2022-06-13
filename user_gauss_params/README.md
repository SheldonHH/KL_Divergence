# Generation of Gauss Params for Training Device

- Input:  raw data which format of `userx_data.csv`
- Output: gauss params for each dimension of the user's data

Required File Format:
`user_x.csv`

## Required Directory Structure

```bash
data 
│   user_x.csv (raw data)
└───features
│   └───freq 
│       │ 
```

## Installation

```bash
cd py
pip3 isntall -r requirements.txt
```

### Usage

```golang
go run main.go
```

#### Developer Notes

Intermediated Files except raw data and final result

```bash
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

```golang
go mod init userGenerateGauss
```
