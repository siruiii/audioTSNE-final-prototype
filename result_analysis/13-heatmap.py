import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke

# List of JSON file paths
file_paths = [
    '../console_log/1-A1-merge.json', 
    '../console_log/2-A1-merge.json', 
    '../console_log/3-A1-merge.json',
    '../console_log/4-A1-merge.json',
    # '../console_log/5-A1-merge.json',
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

filename = file_paths[0].split('/')[-1]
config = filename.split('-')[1]
all_data = []

cluster_colors = {-1: 'black', 0: '#9468B8', 1: '#0079B1', 2: '#23A03A',  3: '#FF7C27'}
if config == 'A1':
    cluster_handlers = {-1: "noise", 0: "Singing", 1: "Oral Narrative, Clapping", 2: "Instrumental Music 1", 3: "Instrumental Music 2"}
elif config == 'A2':
    cluster_handlers = {-1: "noise", 0: "Clapping", 1: "Singing(female & male)", 2: "Singing(female)", 3: "Oral Narrative"}
elif config == 'B1':
    cluster_handlers = {-1: "noise", 0: "Singing", 1: "Reciting"}
elif config == 'B2':
    cluster_handlers = {-1: "noise", 0: "Reciting", 1: "Singing"}

# Read and combine data from each file
for file_path in file_paths:
    with open(file_path, 'r') as file:
        data = json.load(file)
        if isinstance(data, list):
            # Extract coordinates, clusters, and durations
            coords = [item["2D_Coord"] for item in data]
            clusters = [item["Cluster"] for item in data]
            durations = [item["Duration"] for item in data]
            
            # Create a DataFrame for this file and append to the list
            df = pd.DataFrame(coords, columns=['x', 'y'])
            df['Cluster'] = clusters
            df['Duration'] = durations
            all_data.append(df)
            unique_clusters = sorted(set(clusters))
        else:
            raise ValueError(f"Data in file {file_path} is not in the expected format")

# Concatenate all DataFrames
df_all = pd.concat(all_data)

# Calculate total duration for each (x, y) point
df_all['Total_Duration'] = df_all.groupby(['x', 'y'])['Duration'].transform('mean')

# Sort the unique total durations and assign alphas based on their position
sorted_durations = sorted(df_all['Total_Duration'].unique())
duration_to_alpha = {duration: 0.001 + 0.1 * (i / (len(sorted_durations) - 1)) for i, duration in enumerate(sorted_durations)}

# Map the alpha values to the DataFrame
df_all['Alpha'] = df_all['Total_Duration'].map(duration_to_alpha)

# Plot the points
plt.figure(figsize=(12, 8))

# Use scatter plot with color based on cluster and alpha based on duration
sc = plt.scatter(df_all['x'], df_all['y'], c=df_all['Cluster'].map(cluster_colors), alpha=df_all['Alpha'], s=50, edgecolor='k')

# Annotate each point with the total duration
#for i, row in df_all.iterrows():
    #plt.text(row['x'], row['y'], f"{row['Total_Duration']:.1f}", fontsize=8, ha='center', va='center',
             #path_effects=[withStroke(linewidth=1, foreground='white')])

# Add legend for clusters
handles = [plt.Rectangle((0,0),1,1, color=cluster_colors[cluster]) for cluster in unique_clusters if cluster != -1]
plt.legend(handles, [f'{cluster_handlers[cluster]}' for cluster in unique_clusters if cluster != -1], fontsize=12)

plt.xticks([])
plt.yticks([])

plt.show()
