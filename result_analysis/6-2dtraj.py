import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize, BoundaryNorm
from matplotlib.cm import ScalarMappable

file_path = '../console_log/13-A1-merge.json'

# Extract the filename from the path
filename = file_path.split('/')[-1]  # '7-A2-merge.json'

# Extract the part between the first and second hyphen
config = filename.split('-')[1]  # 'A2'

# Load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Extracting the 2D coordinates, cluster information, and sequence
x_coords = np.array([item["2D_Coord"][0] for item in data])
y_coords = np.array([item["2D_Coord"][1] for item in data])
clusters = np.array([item["Cluster"] for item in data])
sequences = np.array([item["Sequence"] for item in data]) 
durations = np.array([item['Duration'] for item in data])

# Create a color map for clusters
unique_clusters = np.unique(clusters)
cmap = plt.get_cmap('Greys')

cluster_colors = {-1: 'black', 0: '#9468B8', 1: '#0079B1', 2: '#23A03A',  3: '#FF7C27', }

# Define cluster handlers based on config
if (config == 'A1'):
    cluster_handlers = {-1: "noise", 0: "Singing", 1: "Oral Narrative, Clapping", 2: "Instrumental Music 1", 3: "Instrumental Music 2"}
elif (config == 'A2'):
    cluster_handlers = {-1: "noise", 0: "Clapping", 1: "Singing(female & male)", 2: "Singing(female)", 3: "Oral Narrative"}
elif (config == 'B1'):
    cluster_handlers = {-1: "noise", 0: "Singing", 1: "Reciting"}
elif (config == 'B2'):
    cluster_handlers = {-1: "noise", 0: "Reciting", 1: "Singing"}

# Normalize the sequence values for colormap
min_seq = min(sequences)
max_seq = max(sequences)
norm_sequences = 1 - (sequences - min_seq) / (max_seq - min_seq)  # Normalized sequence values between 0 and 1

min_duration = min(durations)
max_duration = max(durations)
normalized_alphas = [(duration - min_duration) / (max_duration - min_duration) for duration in durations]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 7))

previous_color = None

for i, cluster in enumerate(clusters):
    alpha = norm_sequences[i]
    if cluster == -1:
        color = previous_color  # Use the previous color
    else:
        color = cluster_colors[cluster]  # Get color for the current cluster
        previous_color = color  # Update the previous color

    if i !=-1:
        alpha = 1
        ax.plot(x_coords[i:i+2], y_coords[i:i+2], color="black", alpha=norm_sequences[i])
        ax.scatter(x_coords[i], y_coords[i], color=color, s=30, alpha=alpha)
        #ax.scatter(x_coords[i], y_coords[i], color=color, s=30, alpha=normalized_alphas[i])
        # if i == 0:
        #     ax.scatter(x_coords[i], y_coords[i], color="red", s=150, alpha=alpha)
        # if i == len(clusters) // 2:
        #     ax.scatter(x_coords[i+1], y_coords[i+1], color="black", s=150, alpha=alpha)
    else:
        alpha = 0
        ax.plot(x_coords[i:i+2], y_coords[i:i+2], color=color, alpha=alpha)
        ax.scatter(x_coords[i], y_coords[i], color=color, s=30, alpha=alpha)
        #ax.scatter(x_coords[i], y_coords[i], color=color, s=30, alpha=normalized_alphas[i])
        if i == len(clusters) // 2 + 1:
            ax.scatter(x_coords[i], y_coords[i], color="red", s=150, alpha=alpha)
        if i == len(clusters) - 1:
            ax.scatter(x_coords[i], y_coords[i], color="black", s=150, alpha=alpha)

# Add a legend
handles = [plt.Rectangle((0, 0), 1, 1, color=cluster_colors[cluster]) for cluster in unique_clusters if cluster == -2]

# Create start and end point handles
start_handle = plt.Line2D([0], [0], marker="o", color='w', markerfacecolor="red", markersize=10, label='Start Point')
end_handle = plt.Line2D([0], [0], marker="o", color='w', markerfacecolor="black", markersize=10, label='End Point')

handles.append(start_handle)
handles.append(end_handle)

#labels = [f'{cluster_handlers[cluster]}' for cluster in unique_clusters if cluster != -1] + ['Start Point', 'End Point']
labels = ['Start Point', 'End Point']

ax.set_xticks([])
ax.set_yticks([])

#ax.legend(handles, labels, fontsize=15, loc="upper left")

# # Add a color bar for the alphavalues
# def alpha_to_duration(alpha):
#     return min_duration + alpha * (max_duration - min_duration)

# # Set the color bar to have 5 discrete blocks
# n_blocks = 5
# bounds = np.linspace(0, 1, n_blocks + 1)
# norm = BoundaryNorm(boundaries=bounds, ncolors=256)
# alpha_cmap = plt.get_cmap('Greys')
# sm = ScalarMappable(cmap=alpha_cmap, norm=norm)
# sm.set_array([])

# # Adjust the position and size of the color bar
# cbar = fig.colorbar(sm, ax=ax, pad=0.05, aspect=10, ticks=bounds, orientation='vertical', 
#                     fraction=0.03, anchor=(1.0, 0.5))
# cbar.set_label('Dwell Time',fontsize=15)

# # Set tick labels for the discrete blocks
# cbar.set_ticklabels([f'{alpha_to_duration(bound):.0f}' for bound in bounds])

plt.show()
