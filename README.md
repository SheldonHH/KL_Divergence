# Introduction

Checkout [Dynamic Fit Branch](https://github.com/SheldonHH/KL_Divergence/tree/dynamic)
This article will focus on introduce the rationale of application, for detailed installation and running of application, please see:
See More:

1. [user_gauss_params](user_gauss_params/README.md)
2. [server_entropy_percent](server_entropy_percent/README.md)

## 1. Training device generate Gauss parameters based on users’ raw data

Input: user's raw MINIST data  
Output: Gaussian Mixture after CNN processing

### 1.1 Image Features Extraction

How can we represent the image as numbers? Well, the image actually consists of numbers, and each number represents the colors or brightness. Unfortunately, this representation is unsuitable when we want to do some machine learning tasks, for example, image clustering.

Clustering is basically a machine learning task where we group the data based on their features, and each group consists of data similar to each other. When we want to cluster data like an image, we have to change its representation into a one-dimensional vector.

But we cannot just convert the image as the vector directly. Let’s say you have a color image, which has the size of 512x512 pixels and three channels, where each channel represents the color of red, green, and blue.

When we convert the three-dimensional matrix into a one-dimensional vector, the vector will consist of 786.432 values. That’s a huge number!

If we use all of them, it will make our computer slow to process the data. Therefore, we need a method to extract those features, and that’s where the convolutional neural network (CNN) comes in.

## Convolutional Neural Network

A CNN is one of the most popular deep learning models. This model is mostly used for image data. This model will do a convolution process on the image, where it filters the image with a thing called kernel so we can get a pattern from it.

A CNN can catch high, medium, and even low-level features, thanks to its hierarchical structure and various filter size. Also, it can compress the information into a small size by using a mechanism called pooling.

The advantage of the CNN model is that it can catch features regardless of the location. Therefore, this neural network is the perfect type to process the image data, especially for feature extraction [1][2].

## K-Means Algorithm

After we extract the feature vector using CNN, now we can use it based on our purpose. In this case, we want to cluster the image into several groups. How can we group the images?

We can use an algorithm called K-Means. At first, the K-Means will initialize several points called centroid. Centroid is a reference point for data to get into a group. We can initialize centroid as many as we want.

After we initialize the centroid, we will measure the distance of each data to each centroid. If the distance value is the smallest, then the data belongs to the group. It changes over time until the clusters not change significantly.

To measure the distance, we can use a formula called euclidean distance. The formula looks like this,

![.](https://miro.medium.com/max/548/1*n9hOsxqF9Yc0mQstKpQ6DQ.png)

### 1.2 Gaussian Mixture Model Fit

1. Training device generate Gauss parameters based on users’ raw data
    1. trimmed each dimension of the raw data
    2. calculate the frequency for each trimmed dimension data
    3. curve_fit based on frequency of each

        1, the second derivatives of MSE of count-incremental curve_fit generally follow the Elbow Methods.
        2, here is a hybrid solution with Elbow
            1. generate gauss from 1 gauss to 10 gauss,
            2. then keep increasing the gauss numbers and perform curve_fit, record the MSE with corresponding number of gauss functions in list.
                1. stop on which the first order derivative of MSE become negative or the the second order derivatives of MSE less than 10%
            3. Choose the number of Gauss with smallest MSE, and save the corresponding params to JSON

References:

[1] [Simonyan, K., & Zisserman, A. (2015). Very Deep Convolutional Networks for Large-Scale Image Recognition. ArXiv:1409.1556](http://arxiv.org/abs/1409.1556).

[2] [VGG16 — Convolutional Network for Classification and Detection. (2018, November 20)](https://neurohive.io/en/popular-networks/vgg16/)

## 2. Generate Gauss(Training Device) and Entropy Percentage(server)

1. Contribution Calculation:

- Input: Individual users' Gaussian
- Output: Percentage of each user's entropy

2. Voting Device Server generate Entropy weight percentage based on all Training Devices’ Gauss parameters

    1. Consolidate all users params to one consolidated Gauss Params
    2. Generate Entropy from by integrating max and min to wit Gauss Params

- Input: consolidated gauss params file address
- Output: entropy percentage for each user
