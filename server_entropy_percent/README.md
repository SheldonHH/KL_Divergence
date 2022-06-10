Input: consolidated gauss params file address
Output: entropy percentage for each user 


### Required Directory Structure:
```
data 
│   └───users_individual_gauss 
│   │     user_1_features_gauss.json
│   │     user_2_features_gauss.json
│   │     user_3_features_gauss.json
|   |     └───consolidated  
|   |                     |   entropysum_percent.json  
```

## Installation 
```
cd py
pip3 isntall -r requirements.txt
```

### How to Run the ServerGenerateEntropy
```
go run main.go
```


# Introducation of Generating Gauss(Training Device) and Entropy Percentage(server)

[Golang-Python](https://github.com/SheldonHH/KL_Divergence/tree/dynamic) 

1. Training device generate Gauss parameters based on users’ raw data
    1. trimmed each dimension of the raw data
    2. calculate the frequency for each trimmed dimension data
    3. curve_fit based on frequency of each trimmed dimensional data
        1. Caveat: the second derivatives of MSE of count-incremental curve_fit doesn’t strictly follow the Elbow Methods.
        2. Hence, by heeding advices from Chengling, here is a hybrid solution with Elbow
            1. generate gauss from 1 gauss to 10 gauss, 
            2. then keep increasing the gauss numbers and perform curve_fit, record the MSE with corresponding number of gauss functions in list.
                1. stop on which the first order derivative of MSE become negative or the the second order derivatives of MSE less than 10% 
            3. Choose the number of Gauss with smallest MSE, and save the corresponding params to JSON
    
2.  Voting Device Server generate Entropy weight percentage based on all Training Devices’ Gauss parameters
    1. Consolidate all users params to one consolidated Gauss Params
    2. Generate Entropy from by integrating max and min to wit Gauss Params


```
go mod init server_entropy_percent
go mod tidy
```