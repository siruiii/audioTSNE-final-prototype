import json
import matplotlib.pyplot as plt

# Load data from JSON file
# File path
file_path = '../console_log/7-A1-merge.json'

# Extract the filename from the path
filename = file_path.split('/')[-1]  # '7-A2-merge.json'

# Extract the part between the first and second hyphen
config = filename.split('-')[1]  # 'A2'


# Load JSON data (if needed)
with open(file_path, 'r') as file:
    data = json.load(file)

# Extracting data for plotting
sequences = [entry["Sequence"] for entry in data]
durations = [entry["Duration"] for entry in data]
clusters = [entry["Cluster"] for entry in data]  # Assuming cluster information is available

# Define unique clusters
unique_clusters = sorted(set(clusters))

# Custom color mapping for clusters
cluster_colors = {
    0: '#9468B8', 
    1: '#0079B1', 
    2: '#23A03A',  
    3: '#FF7C27', 
}

# Creating the histogram
plt.figure(figsize=(10, 6))

# Initialize the previous color variable
previous_color = None

# Plot bars with different colors according to clusters
for i, cluster in enumerate(clusters):
    # Check if the cluster is -1 (noise points)
    if cluster == -1:
        color = previous_color  # Use the previous color
    else:
        color = cluster_colors.get(cluster, 'gray')  # Get color for the current cluster
        previous_color = color  # Update the previous color

    plt.bar(sequences[i], durations[i], color=color, edgecolor='black', alpha=0.5)

# Labels and title
plt.ylabel('Dwell Time (in sec)')
plt.grid(axis='y', linestyle='--', alpha=0.7)



# Define a dictionary that maps cluster IDs to their handling functions
if (config == 'A1'):
    cluster_handlers = {-1: "noise", 0: "Singing", 1: "Oral Narrative, Clapping", 2: "Instrumental Music 1", 3: "Instrumental Music 2"}
elif (config == 'A2'):
    cluster_handlers = {-1: "noise", 0: "Clapping", 1: "Singing(female & male)", 2: "Singing(female)", 3: "Oral Narrative"}
elif (config == 'B1'):
    cluster_handlers = {-1: "noise", 0: "Singing", 1: "Reciting"}
elif (config == 'B2'):
    cluster_handlers = {-1: "noise", 0: "Reciting", 1: "Singing"}



# Adding a legend (optional, if you want to keep it)
handles = [plt.Rectangle((0,0),1,1, color=cluster_colors[cluster]) for cluster in unique_clusters if cluster != -1]
plt.legend(handles, [f'{cluster_handlers[cluster]}' for cluster in unique_clusters if cluster != -1])

plt.xticks([])  # Hides the x-axis labels

# Show plot
plt.show()
