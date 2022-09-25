import torch
from torch import nn
from torchvision import models, transforms
import numpy as np
from cv2 import cv2
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



def extract_features_fast(true_datapath, preprocess_alias, rawlens):
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
    new_fea_path = true_datapath+"features/"+preprocess_alias+"/"
    if os.path.isdir(new_fea_path) == False:
        os.mkdir(new_fea_path) # make dir for that user
    # for each raw data
    for i in range(rawlens):
        if os.path.exists(new_fea_path+preprocess_alias+"_features_"+str(i)+".csv") == False:
            print(i)
            jpeg_data_path1 = true_datapath+"image/"+preprocess_alias+"/"+preprocess_alias+"_"+str(i)+".jpeg"
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
            # print(type(features))
            np.savetxt(new_fea_path+preprocess_alias+"_features_group_"+str(i)+".csv", features)


    return features[0]