# Generation of Gauss Params for Training Device

- Input:  raw data which format of `user_x.csv`
- Output: gauss params for each dimension of the user's data `user_1_features_gauss.json`

Required File Format:
`user_x.csv`

## 1. Required Directory Structure

```bash
data 
│   user_x.csv (raw data)
└───features
│   └───freq 
```

## 2. Installation

```bash
cd py
pip3 isntall -r requirements.txt
```

## 3. Usage

```golang
go run main.go
```

## 4. Executation Explain

it will call the main functions in python files below sequentially while generating temporal files (deleted after make used on subsequent file)

1. `tally/csv_to_jpeg.py`: To convert `.csv` format to `.jpeg`
2. `py_torch/pytorch-extractor.py`: extract the features using pytorch
3. `tally/round_data_golang.py`: round raw data to a specific decimal
   - input: `user_gauss_params/data/user_x.csv`
   - Output: `user_gauss_params/data/rounded_user_x.csv`

4. `tally/countFreq_golang.py` generate counts of unique values of rounded raw data in `data,freq` format
   - input: `user_gauss_params/data/rounded_user_x.csv`
   - Output: `user_gauss_params/data/features/freq/user_x_freq.csv`

5. `tally/freq_to_gauss_golang.py` generate the gaussian parameters predicated on step 4.
   - input: `user_gauss_params/data/freq/user_x_freq.csv`
   - Output: `user_gauss_params/data/features/freq/user_x_features_gauss.json`

### Developer Notes

Intermediated Files except raw data and final result

```bash
data 
│   user_x.csv (raw data)
|   user_x.jpeg 
└───features
    │   user_x_feature.csv
    └───freq
        │   user_x_freq.csv
        │   user_x_features_gauss.json (final result)
```

1. preprocess each dimension of user's data to dense_trimmed_user_x_data.csv
2. generate the frequence data for each dimension of the user's data
3. generate gauss params for each dimension of the user's data

```golang
go mod init userGenerateGauss
```
