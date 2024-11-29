import json
from collections import defaultdict

# List of file paths
file_paths = [
    '../console_log/1-A1-merge.json', 
    '../console_log/2-A1-merge.json', 
    '../console_log/3-A1-merge.json',
    #'../console_log/5-A1-merge.json',
    '../console_log/6-A1-merge.json', 
    '../console_log/7-A1-merge.json',
    '../console_log/8-A1-merge.json',
    '../console_log/9-A1-merge.json',
    '../console_log/10-A1-merge.json',
    '../console_log/11-A1-merge.json',
    '../console_log/12-A1-merge.json',
    '../console_log/13-A1-merge.json',
    '../console_log/14-A1-merge.json', 
    '../console_log/15-A1-merge.json',
    '../console_log/16-A1-merge.json'
]


# Dictionary to hold total duration per cluster for each file
file_cluster_duration = {}

# Read each file and accumulate durations
for file_path in file_paths:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Dictionary to hold total duration per cluster for the current file
            cluster_duration = defaultdict(float)

            # Assuming data contains a list of events, each with a cluster and duration
            for event in data:
                cluster = event.get('Cluster')
                duration = event.get('Duration', 0)

                # Accumulate total duration for the cluster in the current file
                cluster_duration[cluster] += duration

            # Store the total duration per cluster for the current file
            file_cluster_duration[file_path] = dict(cluster_duration)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")

# Output total duration per cluster for every file
for file, cluster_data in file_cluster_duration.items():
    for cluster, duration in cluster_data.items():
        print(f"{cluster}, {duration}")