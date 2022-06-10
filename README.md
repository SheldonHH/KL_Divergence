# Introduction
Checkout [Dynamic Fit Branch](https://github.com/SheldonHH/KL_Divergence/tree/dynamic) 
This article will focus on introduce the rationale of application, for detailed installation and running of application, please see:
See More: 
1. [user_gauss_params](user_gauss_params/README.md)
2. [server_entropy_percent](server_entropy_percent/README.md)
### 1. Training device generate Gauss parameters based on users’ raw data 
Input: user's raw MINIST data
Output: Gaussian Mixture after CNN processing
1. Training device generate Gauss parameters based on users’ raw data
    1. trimmed each dimension of the raw data
    2. calculate the frequency for each trimmed dimension data
    3. curve_fit based on frequency of each trimmed dimensional data
    Image Feature Extraction Using PyTorch
        1. Caveat: the second derivatives of MSE of count-incremental curve_fit doesn’t strictly follow the Elbow Methods.
        2. Hence, by heeding advices from Chengling, here is a hybrid solution with Elbow
            1. generate gauss from 1 gauss to 10 gauss, 
            2. then keep increasing the gauss numbers and perform curve_fit, record the MSE with corresponding number of gauss functions in list.
                1. stop on which the first order derivative of MSE become negative or the the second order derivatives of MSE less than 10% 
            3. Choose the number of Gauss with smallest MSE, and save the corresponding params to JSON
References
[1] Simonyan, K., & Zisserman, A. (2015). Very Deep Convolutional Networks for Large-Scale Image Recognition. ArXiv:1409.1556 [Cs]. http://arxiv.org/abs/1409.1556
[2] VGG16 — Convolutional Network for Classification and Detection. (2018, November 20). https://neurohive.io/en/popular-networks/vgg16/



### 2. Generate Gauss(Training Device) and Entropy Percentage(server)
contribution calculation：
INPUT: Individual users' Gaussian
OUTPUT: Percentage of each user's Entropy
2.  Voting Device Server generate Entropy weight percentage based on all Training Devices’ Gauss parameters
    1. Consolidate all users params to one consolidated Gauss Params
    2. Generate Entropy from by integrating max and min to wit Gauss Params

Input: consolidated gauss params file address
Output: entropy percentage for each user 


