from sklearn.cluster import KMeans
import pandas as pd

# Initialize the model
model = KMeans(n_clusters=5, random_state=42)

# Fit the data into the model
model.fit(features)

# Extract the labels
labels = model.labels_

print(labels) # [4 3 3 ... 0 0 0]



sample_submission = pd.read_csv('sample_submission.csv')
new_submission = sample_submission
new_submission['label'] = labels
new_submission.to_csv('submission_1.csv', index=False)