import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

file_paths = [
    '../console_log/13-A1-merge.json',
]

cluster_colors = {
    0: '#9468B8',  # Color for cluster 0
    1: '#0079B1',  # Color for cluster 1
    2: '#23A03A',  # Color for cluster 2
    3: '#FF7C27',  # Color for cluster 3
}

# Function to calculate Euclidean distance between two 3D points
def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

# Loop over each file path
for i, file_path in enumerate(file_paths):
    # Extract the filename and tester information
    filename = file_path.split('/')[-1]
    tester = filename.split('-')[0]  # Extracts tester information
    
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Sort the data by 'Sequence' to ensure proper accumulation over time
    data_sorted = sorted(data, key=lambda x: x['Sequence'])
    
    # Extract point3D coordinates, duration, and cluster information
    points = [(
        entry['point3d'][0],
        entry['point3d'][1],
        entry['point3d'][2]
    ) for entry in data_sorted]
    
    durations = [entry['Duration'] for entry in data_sorted]
    clusters = [entry['Cluster'] for entry in data_sorted]  # Assuming each entry has a 'Cluster' key
    
    # Calculate cumulative duration
    cumulative_durations = np.cumsum(durations)
    
    # Calculate step distances between consecutive points
    distances = [calculate_distance(points[i], points[i+1]) for i in range(len(points) - 1)]
    
    # Use the cumulative duration as x-axis (excluding the last point since distance is between pairs)
    cumulative_durations = cumulative_durations[:-1]
    
    # Create a new figure for each plot
    fig, ax = plt.subplots(figsize=(16, 2))
    
    # Add background color based on clusters without redrawing the same cluster
    previous_cluster = clusters[0]  # Initialize with the first cluster
    patch_start = cumulative_durations[0]  # Start of the first patch
    
    for j in range(1, len(cumulative_durations)):
        current_cluster = clusters[j]
        # Draw a patch if the cluster changes
        if current_cluster != previous_cluster:
            # Draw the patch for the previous cluster
            color = cluster_colors.get(previous_cluster, '#FFFFFF')  # Default to white if cluster is not in the color map
            ax.add_patch(patches.Rectangle(
                (patch_start, min(distances) - 1),  # (x, y) starting position
                cumulative_durations[j] - patch_start,  # width
                max(distances) - min(distances) + 2,  # height
                color=color,
                alpha=0.3  # Adjust transparency as needed
            ))
            # Update the start position and previous cluster
            patch_start = cumulative_durations[j]
            previous_cluster = current_cluster

    # Draw the last patch if needed
    color = cluster_colors.get(previous_cluster, '#FFFFFF')
    ax.add_patch(patches.Rectangle(
        (patch_start, min(distances) - 1),  # (x, y) starting position
        cumulative_durations[-1] - patch_start,  # width
        max(distances) - min(distances) + 2,  # height
        color=color,
        alpha=0.3  # Adjust transparency as needed
    ))

    # Plot the step distances
    ax.plot(cumulative_durations, distances, marker='o', linestyle='-', color='black', markerfacecolor='none', markersize=5)
    ax.set_xlabel('Time (in sec)', fontsize=15)
    ax.set_ylabel('Step Distance', fontsize=15)
    ax.set_xticks([0,60,120])
    # Show the plot
    plt.tight_layout()
    plt.show()
