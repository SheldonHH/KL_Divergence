import torch
from torch import optim, nn
from torchvision import models, transforms
from tqdm import tqdm
import numpy as np
from os import listdir
from os.path import isfile, join
from cv2 import cv2
import pandas as pd

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

# Initialize the model
model = models.vgg16(pretrained=True)
new_model = FeatureExtractor(model)

# Change the device to GPU
device = torch.device('cuda:0' if torch.cuda.is_available() else "cpu")
new_model = new_model.to(device)





# Transform the image, so it becomes readable with the model
transform = transforms.Compose([
  transforms.ToPILImage(),
  transforms.CenterCrop(512),
  transforms.Resize(448),
  transforms.ToTensor()                              
])
# Will contain the feature
features = []

# Iterate each image

# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# for i in tqdm(sample_submission.ImageID):
#     # Set the image path
#     path = os.path.join('data', 'test', str(i) + '.jpg')
    # Read the file
path = r"/root/KL_Divergence/user_gauss_params/data/uniform/user_1.jpeg"
img = cv2.imread(path)
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

pd.DataFrame(features).to_csv("/root/KL_Divergence/user_gauss_params/data/uniform/features/user_1_features.csv", header=False)
np.savetxt("/root/KL_Divergence/user_gauss_params/data/uniform/features/user_1_features.txt",features)