import json
import numpy as np
import matplotlib.pyplot as plt

# Define a specific list of 5 colors
colors = {0: '#9468B8', 1: '#0079B1', 2: '#23A03A',  3: '#FF7C27'}  # Blue, Green, Red, Cyan, Magenta

file_paths = [
    #'../console_log/1-A1-merge.json', 
    #'../console_log/2-A1-merge.json', 
    #'../console_log/3-A1-merge.json', 
    #'../console_log/5-A1-merge.json',
    #'../console_log/6-A1-merge.json',
    #'../console_log/7-A1-merge.json',
    '../console_log/8-A1-merge.json',
    '../console_log/8-A1-merge.json',
    '../console_log/8-A1-merge.json',
    '../console_log/8-A1-merge.json',
    #'../console_log/12-A1-merge.json',
    #'../console_log/13-A1-merge.json',
    #'../console_log/14-A1-merge.json', 
    #'../console_log/15-A1-merge.json',
    #'../console_log/16-A1-merge.json'
]

# Create a new figure
plt.figure(figsize=(12, 8))

# Initialize a dictionary to hold the cluster-color mapping
cluster_color_map = {}
color_index = 0

# First pass to determine all unique clusters and assign colors
for file_path in file_paths:
    try:
        filename = file_path.split('/')[-1]
        tester = filename.split('-')[0]

        # Read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Check if data is not empty
        if not data:
            continue
        
        # Check the structure of the data
        required_fields = {'Sequence', 'Duration', 'Cluster'}
        if not all(field in data[0] for field in required_fields):
            continue

        # Filter out entries with Cluster = -1
        data_filtered = [entry for entry in data if entry['Cluster'] != -1]

        # If no valid data after filtering, skip the file
        if not data_filtered:
            continue

        # Get unique clusters
        clusters = {entry['Cluster'] for entry in data_filtered}
        for cluster in clusters:
            if cluster not in cluster_color_map:
                cluster_color_map[cluster] = colors[color_index % len(colors)]
                color_index += 1

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Second pass to plot data using the cluster-color mapping
for file_index, file_path in enumerate(file_paths):
    try:
        filename = file_path.split('/')[-1]
        tester = filename.split('-')[0]

        # Read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Check if data is not empty
        if not data:
            continue
        
        # Check the structure of the data
        required_fields = {'Sequence', 'Duration', 'Cluster'}
        if not all(field in data[0] for field in required_fields):
            continue

        # Filter out entries with Cluster = -1
        data_filtered = [entry for entry in data if entry['Cluster'] != -1]

        # If no valid data after filtering, skip the file
        if not data_filtered:
            continue

        # Sort the filtered data by 'Sequence'
        data_sorted = sorted(data_filtered, key=lambda x: x['Sequence'])

        # Prepare data for plotting
        sequences = [entry['Sequence'] for entry in data_sorted]
        durations = [entry['Duration'] for entry in data_sorted]
        clusters = [entry['Cluster'] for entry in data_sorted]

        # Calculate cumulative dwell time
        cumulative_dwell_time = np.cumsum(durations)

        # Plot each data point
        for idx in range(len(clusters)):
            cluster = clusters[idx]
            color = cluster_color_map.get(cluster, 'k')  # Default to black if cluster color is missing
            plt.plot(cumulative_dwell_time[idx:idx+1], [file_index] * len(cumulative_dwell_time[idx:idx+1]), marker='o', linestyle='-', color=color, markersize=5)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Add labels and title
plt.title('Dwell Time Change with File Index')
plt.xlabel('Cumulative Dwell Time')
plt.ylabel('File Index')
plt.yticks(ticks=range(len(file_paths)), labels=[f'{i+1}' for i in range(len(file_paths))])
plt.tight_layout()

# Show the plot
plt.show()
