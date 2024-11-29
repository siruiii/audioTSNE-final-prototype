import json
import numpy as np
import matplotlib.pyplot as plt

file_paths = [
    '../console_log/6-A1-merge.json',
    '../console_log/6-B1-merge.json'
] 

cluster_colors = {-1:'black',0: '#9468B8', 1: '#0079B1', 2: '#23A03A', 3: '#FF7C27'}

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
    
    # Prepare data for plotting
    sequences = [entry['Sequence'] for entry in data_sorted]
    durations = [entry['Duration'] for entry in data_sorted]
    clusters = [entry['Cluster'] for entry in data_sorted]
    
    # Calculate cumulative dwell time
    cumulative_dwell_time = np.cumsum(durations)
    
    # Create a new figure for each plot
    plt.figure(figsize=(16, 2))
    ax = plt.gca()
    
    # Add background color based on clusters
    prev_cluster = clusters[0]
    start_time = cumulative_dwell_time[0]
    

    for j in range(0, len(clusters)):
        if clusters[j] != prev_cluster:
            ax.axvspan(start_time, cumulative_dwell_time[j], color=cluster_colors[prev_cluster], alpha=0.3)
            start_time = cumulative_dwell_time[j]
            prev_cluster = clusters[j]
    
    # Add the last region
    ax.axvspan(start_time, cumulative_dwell_time[-1], color=cluster_colors[prev_cluster], alpha=0.3)
    
    # Plot the cumulative dwell time against dwell time
    plt.plot(cumulative_dwell_time, durations, marker='o',linestyle='-',color='black', markerfacecolor='none', markersize=2)
    plt.xlabel('Time',fontsize=15)
    plt.ylabel('Dwell Time',fontsize=15)
    plt.tight_layout()
    plt.show()
