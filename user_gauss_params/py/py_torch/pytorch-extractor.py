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
    args = sys.argv[1:]
    raw_csv_path1 = args[0]
    print(args)
    jpeg_data_path1 = args[0][0:args[0].rindex('.')]+".jpeg"
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
    # Will contain the feature
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

    # Convert to NumPy Array
    features = np.array(features)
    print("features", len(features[0]))

    path = raw_csv_path1[0:raw_csv_path1.rindex('/')+1]
    username = raw_csv_path1[raw_csv_path1.rindex('/')+1: raw_csv_path1.rindex('.')]
    pd.DataFrame(features).T.to_csv(path+username+"_features.csv", header=False, index=False)
    os.remove(jpeg_data_path1)
    # np.savetxt("/root/KL_Divergence/user_gauss_params/data/uniform/features/user_1_features.txt",features)

if __name__ == "__main__":
    main()
