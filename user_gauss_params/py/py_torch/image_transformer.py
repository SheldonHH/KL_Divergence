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
for i in tqdm(sample_submission.ImageID):
	# Set the image path
  path = os.path.join('data', 'test', str(i) + '.jpg')
  # Read the file
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