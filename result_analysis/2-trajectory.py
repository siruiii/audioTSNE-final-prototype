import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Load the JSON file
with open('merge_result1.json', 'r') as file:
    data = json.load(file)

# Extracting the 3D coordinates and cluster information
x_coords = np.array([-item["point3d"][0] for item in data])
y_coords = np.array([item["point3d"][2] for item in data])
z_coords = np.array([item["point3d"][1] for item in data])
clusters = np.array([item["Cluster"] for item in data])

# Create a color map for clusters
unique_clusters = np.unique(clusters)
cmap = plt.get_cmap('viridis')  # You can choose different colormaps
colors = {cluster: cmap(i / len(unique_clusters)) for i, cluster in enumerate(unique_clusters)}

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each segment with color based on clusters
for i in range(len(x_coords) - 1):
    color = colors[clusters[i]] if clusters[i] == clusters[i + 1] else colors[clusters[i]]  # Color based on cluster
    ax.plot(x_coords[i:i+2], y_coords[i:i+2], z_coords[i:i+2], color=color, marker='o')

# Labeling the axes
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

# Adding a title
ax.set_title('3D Trajectory Plot with Cluster-Based Coloring')

# Add a legend
handles = [plt.Line2D([0], [0], color=colors[cluster], lw=2) for cluster in unique_clusters]
labels = [f'Cluster {cluster}' for cluster in unique_clusters]
ax.legend(handles, labels, title='Clusters')

# Show plot
plt.show()
