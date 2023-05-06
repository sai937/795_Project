import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load gaze data from CSV file
df = pd.read_csv('eye_tracking_data.csv', header=None, names=['gazeData'])
df['gazeData'] = df['gazeData'].apply(lambda x: eval(x)) # Convert string to dictionary

# Extract gaze points from dictionary
gazePoints = []
for data in df['gazeData']:
    if data['x'] != None and data['y'] != None:
        gazePoints.append((data['x'], data['y']))

# Convert gaze points to numpy array
gazePoints = np.array(gazePoints)

# Calculate statistics
mean = np.mean(gazePoints, axis=0)
median = np.median(gazePoints, axis=0)
mode = stats.mode(gazePoints, axis=0)[0][0]
std_dev = np.std(gazePoints, axis=0)
min_vals = np.min(gazePoints, axis=0)
max_vals = np.max(gazePoints, axis=0)
q1 = np.quantile(gazePoints, 0.25, axis=0)
q3 = np.quantile(gazePoints, 0.75, axis=0)
iqr = q3 - q1

# Identify outliers
outliers = []
for point in gazePoints:
    if (point[0] < (q1[0] - 1.5 * iqr[0])) or (point[0] > (q3[0] + 1.5 * iqr[0])) or \
       (point[1] < (q1[1] - 1.5 * iqr[1])) or (point[1] > (q3[1] + 1.5 * iqr[1])):
        outliers.append(point)
outliers = np.array(outliers)

# Create scatter plot with statistics and outliers
fig, ax = plt.subplots(figsize=(10, 8))
sns.scatterplot(x=gazePoints[:, 0], y=gazePoints[:, 1], ax=ax, s=5)
ax.set_facecolor('gray')
plt.scatter(mean[0], mean[1], color='green', s=200, marker='o')
plt.scatter(median[0], median[1], color='blue', s=200, marker='o')
plt.scatter(mode[0], mode[1], color='orange', s=200, marker='o')
plt.scatter(outliers[:, 0], outliers[:, 1], color='red', s=10)
plt.title('Gaze Point Statistics')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.legend(['Gaze Points', 'Mean', 'Median', 'Mode', 'Outliers'])
plt.show()
