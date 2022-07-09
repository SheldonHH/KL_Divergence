import timeit
from tally import csv_to_jpeg
from py_torch.FeatureExtractor import extract_features
from tally import round_data_golang
from tally import countFreq_golang
from tally import freq_to_gauss_golang
import numpy as np

import pandas as pd
# from tally import features_extractor

import torch
from torch import optim, nn
from torchvision import models, transforms
from tqdm import tqdm
import numpy as np
from os import listdir
from os.path import isfile, join
from cv2 import cv2
import pandas as pd
import sys
import os
model = models.vgg16(pretrained=True)


class FeatureExtractor(nn.Module):
    def __init__(self, model):
        super(FeatureExtractor, self).__init__()
        # Extract VGG-16 Feature Layers
        self.features = list(model.features)
        self.features = nn.Sequential(*self.features)
        # Extract VGG-16 Average Pooling Layer
        self.pooling = model.avgpool
        # Convert the image into one-dimensional vector
        self.flatten = nn.Flatten()
        # Extract the first part of fully-connected layer from VGG16
        self.fc = model.classifier[0]

    def forward(self, x):
        # It will take the input 'x' until it returns the feature vector called 'out'
        out = self.features(x)
        out = self.pooling(out)
        out = self.flatten(out)
        out = self.fc(out)
        return out


def main():
    # Two Inputs
    numpy_array = np.loadtxt(
        "/root/KL_Divergence/user_gauss_params/data/user_4.csv", delimiter=",")
    user_name = "user_4"
    # for i in range(len(numpy_array)):
    #     dynamic_gauss([numpy_array[i]], user_name, str(i))
    
    real_raw_csv_argv = [
        "/root/KL_Divergence/user_gauss_params/data/"]
    raw_csv_argv = [real_raw_csv_argv[0]+user_name+".csv"]
    raw_csv_path1 = raw_csv_argv[0]


    nested_features = []
    args = raw_csv_argv
    raw_csv_path1 = args[0]
    # print(args)
    model = models.vgg16(pretrained=True)
    new_model = FeatureExtractor(model)
    device = torch.device('cuda:0' if torch.cuda.is_available() else "cpu")
    new_model = new_model.to(device)
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.CenterCrop(512),
        transforms.Resize(448),
        transforms.ToTensor()
    ])
    for i in range(len(numpy_array)):
        # if i <= 2:
        # single_file_feature = dynamic_gauss(
        #     [numpy_array[i]], user_name, str(i))
        # single_file_feature = obtain_features(raw_csv_argv, str(i))
        jpeg_data_path1 = args[0][0:args[0].rindex('.')]+"_"+str(i)+".jpeg"
        features = []
        img = cv2.imread(jpeg_data_path1)
        # Transform the image

        img = transform(img)
        # Reshape the image. PyTorch model reads 4-dimensional tensor
        # [batch_size, channels, width, height]
        img = img.reshape(1, 3, 448, 448)
        img = img.to(device)
        # We only extract features, so we don't need gradient
        with torch.no_grad():
            # Extract the feature from the image
            feature = new_model(img)
        # Convert to NumPy Array, Reshape it, and save it to features variable
        features.append(feature.cpu().detach().numpy().reshape(-1))
        
        nested_features.append(features)
        print(i)
    return
        
        # else:
        #     break



    path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    username = raw_csv_path1[raw_csv_path1.rindex(
        '/')+1: raw_csv_path1.rindex('.')]
    np.savetxt(user_name+'_joints.csv', nested_features)
    print(len(nested_features))
    for idx, col in enumerate(np.array(nested_features).T):
        print(col.tolist())
        freq_to_gauss_golang.freq_to_gauss(
            raw_csv_argv, len(numpy_array), col, str(idx))
        # break

    # print(len(nested_features[0]))

    # pd.DataFrame(nested_features).T.to_csv(path+username+"_joints_"+".csv", header=False, index=False)


def obtain_features(raw_csv_argv, index_of_image):
    features = []
    args = raw_csv_argv
    jpeg_data_path1 = args[0][0:args[0].rindex('.')]+"_"+index_of_image+".jpeg"
    img = cv2.imread(jpeg_data_path1)
    # Transform the image

    img = transform(img)
    # Reshape the image. PyTorch model reads 4-dimensional tensor
    # [batch_size, channels, width, height]
    img = img.reshape(1, 3, 448, 448)
    img = img.to(device)
    # We only extract features, so we don't need gradient
    with torch.no_grad():
        # Extract the feature from the image
        feature = new_model(img)
    # Convert to NumPy Array, Reshape it, and save it to features variable
    features.append(feature.cpu().detach().numpy().reshape(-1))
    # print(type(features))
    # Convert to NumPy Array
    # features = np.array(features)
    # print("features", len(features[0]))

    stop = timeit.default_timer()
    print('Time: ', stop - start)
    return features[0]


def dynamic_gauss(numpy_array, user_name, index_of_image):
    # print(raw_csv_argv)
    # raw_data_len = csv_to_jpeg.csv_to_jpeg(numpy_array, raw_csv_argv,index_of_image)
    raw_csv_argv = [
        "/root/KL_Divergence/user_gauss_params/data/"+user_name+".csv"]
    return extract_features(raw_csv_argv, index_of_image)
    # print(single_file_feature)

    # round_data_golang.round_data(raw_csv_argv)
    # countFreq_golang.count_freq(raw_csv_argv)
    # freq_to_gauss_golang.freq_to_gauss(raw_csv_argv, raw_data_len)


if __name__ == "__main__":
    main()
