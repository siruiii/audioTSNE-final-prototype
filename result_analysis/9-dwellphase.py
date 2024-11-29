import json
import numpy as np
import matplotlib.pyplot as plt

file_paths = [
    '../console_log/1-A2-merge.json', 
    '../console_log/2-A2-merge.json', 
    '../console_log/3-A2-merge.json',
    '../console_log/4-A2-merge.json',
    '../console_log/5-A2-merge.json',
    '../console_log/6-A2-merge.json', 
    '../console_log/7-A2-merge.json',
    '../console_log/8-A2-merge.json',
    '../console_log/9-A2-merge.json',
    '../console_log/10-A2-merge.json',
    '../console_log/11-A2-merge.json',
    '../console_log/12-A2-merge.json',
    '../console_log/13-A2-merge.json',
    '../console_log/14-A2-merge.json', 
    '../console_log/15-A2-merge.json',
    '../console_log/16-A2-merge.json'
]

cluster_colors = {-1: 'black', 0: '#9468B8', 1: '#0079B1', 2: '#23A03A', 3: '#FF7C27'}

# Initialize plot
plt.figure(figsize=(12, 8))


# Loop over each file path
for file_path in file_paths:
    # Extract the filename and tester information
    filename = file_path.split('/')[-1]
    tester = filename.split('-')[0]  # Extracts tester information
    
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Sort the data by 'Sequence' to ensure proper accumulation over time
    data_sorted = sorted(data, key=lambda x: x['Sequence'])
    
    # Filter data based on the sequence threshold
    data_filtered = [entry for entry in data_sorted if entry['Sequence']]
    
    # Prepare data for plotting
    sequences = [entry['Sequence'] for entry in data_filtered]
    durations = [entry['Duration'] for entry in data_filtered]
    clusters = [entry['Cluster'] for entry in data_filtered]
    
    # Calculate cumulative dwell time
    cumulative_dwell_time = np.cumsum(durations)
    
    # Plot data
    plt.scatter(cumulative_dwell_time, sequences, c=[cluster_colors[c] for c in clusters], label=tester, alpha=0.6, edgecolors='w')

# Add plot details
plt.ylabel('Sequence')
plt.xlabel('Cumulative Duration')
plt.title('Cumulative Duration vs Sequence by Cluster (Limited to Sequence ≤ 60)')
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()
