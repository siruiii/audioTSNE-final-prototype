import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Patch
from matplotlib.colors import Normalize, BoundaryNorm
from matplotlib.cm import ScalarMappable

# Load JSON data from a file
file_path = '../console_log/16-B2-merge.json'  # Replace with the path to your JSON file

# Extract the filename from the path
filename = file_path.split('/')[-1]  # '7-A2-merge.json'

# Extract the part between the first and second hyphen
config = filename.split('-')[1]  # 'A2'

with open(file_path, 'r') as file:
    data = json.load(file)

# Extract 3D points, clusters, and durations
points_3d = [np.array(item['point3d']) for item in data]
clusters = [int(item['Cluster']) for item in data]  # Assuming each item has a 'Cluster' key
durations = [item['Duration'] for item in data]  # Assuming each item has a 'Duration' key

# Calculate distances between consecutive points
distances = []
for i in range(len(points_3d) - 1):
    distance = np.linalg.norm(points_3d[i + 1] - points_3d[i])
    distances.append(distance)

# Print distances in their original order
print("Distances between consecutive points:")
for i, distance in enumerate(distances):
    print(f"Distance {i + 1}: {distance}")

# Count occurrences of each cluster
cluster_counts = {cluster: clusters.count(cluster) for cluster in set(clusters)}
total_count = len(clusters)

# Calculate percentages for each cluster
cluster_percentages = {cluster: (count / total_count) * 100 for cluster, count in cluster_counts.items()}

# Calculate total duration for each cluster
cluster_durations = {cluster: sum(duration for i, duration in enumerate(durations) if clusters[i] == cluster) for cluster in set(clusters)}

# Normalize durations for alpha values
min_duration = min(durations)
max_duration = max(durations)
normalized_alphas = [(duration - min_duration) / (max_duration - min_duration) for duration in durations]

# Create a function to convert normalized alpha values to duration values
def alpha_to_duration(alpha):
    return min_duration + alpha * (max_duration - min_duration)

# Create a figure and axis
fig, ax = plt.subplots()

unique_clusters = np.unique(clusters)
cmap = plt.get_cmap('viridis')  # You can choose different colormaps

# Track the start of each cluster for background coloring
start_idx = 0
previous_color = None

# Create a dictionary to store patches for the legend
legend_patches = {}

cluster_colors = {
    0: '#0079B1', 
    1: '#9468B8', 
    2: '#23A03A',  
    3: '#FF7C27', 
}
if (config=='A1'):
    cluster_handlers = {
        -1: "noise",
        0: "Singing",
        1: "Oral Narrative, Clapping",
        2: "Instrumental Music 1",
        3: "Instrumental Music 2"
    }
elif (config=='A2'):
    cluster_handlers = {
        -1: "noise",
        0: "Clapping",
        1: "Singing(female & male)",
        2: "Singing(female)",
        3: "Oral Narrative"
    }
elif (config=='B1'):
    cluster_handlers = {
        -1: "noise",
        0: "Singing",
        1: "Reciting"
    }
elif (config=='B2'):
    cluster_handlers = {
        -1: "noise",
        0: "Reciting",
        1: "Singing"
    }

# Create a colormap for the alpha values
norm = Normalize(vmin=0, vmax=1)  # Normalize the alpha values
alpha_cmap = plt.get_cmap('Greys')  # You can choose a different colormap for alpha values
previous_color = None
for i in range(len(distances)):
    if i > 0 and clusters[i - 1] != -1 and clusters[i]!=-1:
        color = cluster_colors[clusters[i]]
        previous_color=cluster_colors[clusters[i]]
    else:
        color = previous_color
    
    alpha = normalized_alphas[i]  # Use the normalized alpha based on duration
    ax.plot([i-1, i], [distances[i-1], distances[i]], marker='o', linestyle='-', color=color, alpha=alpha)

    if clusters[i] == -1 or clusters[i+1] == -1:
       #Skip drawing lines for noise points
        continue
    
    # Check if cluster changes or if it's the last point
    if i == len(distances) - 1 or clusters[i] != clusters[i+1]:
        # Add a background color span for the current cluster
        ax.axvspan(start_idx - 0.5, i + 0.5, color=color, alpha=0.2)
        
        # Add the cluster to the legend dictionary if not already added
        if clusters[i] not in legend_patches and clusters[i]!=-1:
            percentage = cluster_durations[clusters[i]] / sum(cluster_durations.values()) * 100
            # Use cluster_handlers for the legend label
            legend_patches[clusters[i]] = Patch(
                color=cluster_colors[clusters[i]], 
                label=f'{cluster_handlers[clusters[i]]} ({percentage:.1f}%)'
            )
        
        # Update the start index for the next cluster
        start_idx = i + 1

# Sort legend entries by total duration
sorted_legend_patches = sorted(legend_patches.values(), key=lambda p: float(p.get_label().split('(')[-1].replace('%)', '')), reverse=True)

# Add title, labels, and grid
ax.set_xlabel('Spatial Exploration Sequence',fontsize=12)
ax.set_ylabel('Step Distance',fontsize=12)

# Adjust the plot limits to make sure the background colors are fully visible
ax.set_xlim(-0.5, len(distances) - 0.5)
ax.set_ylim(0, max(distances) * 1.1)

# Update legend with sorted entries, skipping noise points
handles = [legend_patches[cluster] for cluster in sorted(legend_patches.keys(), key=lambda x: float(legend_patches[x].get_label().split('(')[-1].replace('%)', '')), reverse=True) if cluster != -1]
plt.legend(handles=handles,loc='upper center',fontsize=12)

# Set the color bar to have 5 discrete blocks
n_blocks = 5
bounds = np.linspace(0, 1, n_blocks + 1)
norm = BoundaryNorm(boundaries=bounds, ncolors=256)
alpha_cmap = plt.get_cmap('Greys')
sm = ScalarMappable(cmap=alpha_cmap, norm=norm)
sm.set_array([])

# Adjust the position and size of the color bar
cbar = fig.colorbar(sm, ax=ax, pad=0.05, aspect=10, ticks=bounds, orientation='vertical', 
                    fraction=0.03, anchor=(1.0, 0.5))
cbar.set_label('Dwell Time',fontsize=12)

# Set tick labels for the discrete blocks
cbar.set_ticklabels([f'{alpha_to_duration(bound):.0f}' for bound in bounds])

# Show the plot
plt.show()
