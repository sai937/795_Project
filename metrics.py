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
sns.kdeplot(x=[x[0] for x in gazePoints], y=[x[1] for x in gazePoints], cmap="Reds", shade=True, shade_lowest=False)

# Calculate metrics
threshold = 0.1 # Set threshold for saliency
salientAreas = [] # List of salient areas
for c in ax.collections:
    paths = c.get_paths()
    for path in paths:
        patch = plt.Polygon(path.vertices, closed=True, fill=True, linewidth=0)
        patch.set_clip_on(False)
        ax.add_patch(patch)
        if c.get_array().max() > threshold:
            salientAreas.append(patch)

totalFixationDuration = 0
totalNumFixations = 0
numFixationsPerArea = []
for area in salientAreas:
    fixationDuration = 0
    numFixations = 0
    for data in df['gazeData']:
        if data['x'] != None and data['y'] != None and area.contains_point((data['x'], data['y'])):
            fixationDuration += data['duration']
            numFixations += 1
    totalFixationDuration += fixationDuration
    totalNumFixations += numFixations
    numFixationsPerArea.append(numFixations)

if totalNumFixations > 0:
    avgFixationDuration = totalFixationDuration / totalNumFixations
else:
    avgFixationDuration = 0

print("Total fixation duration:", totalFixationDuration)
print("Average fixation duration:", avgFixationDuration)
print("Total number of fixations:", totalNumFixations)
print("Number of fixations per area:", numFixationsPerArea)
