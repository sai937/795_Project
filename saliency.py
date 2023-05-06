import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load gaze data from CSV file
df = pd.read_csv('eye_tracking_data.csv', header=None, names=['gazeData'])
df['gazeData'] = df['gazeData'].apply(lambda x: eval(x)) # Convert string to dictionary

# Extract gaze points from dictionary
gazePoints = []
for data in df['gazeData']:
    if data['x'] != None and data['y'] != None:
        gazePoints.append((data['x'], data['y']))

# Create heatmap
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_facecolor('gray')
sns.kdeplot(x=[x[0] for x in gazePoints], y=[x[1] for x in gazePoints], shade=True, thresh=0.05, cmap='inferno')

plt.title('Saliency Heatmap of Resume')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.show()