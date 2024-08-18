import json
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke

# Load t-SNE result from JSON file
with open('../1-mfcc-tsne/peking25-10sec_tsne_results.json', 'r') as file:
    tsne_data = json.load(file)

# Extract the t-SNE points and paths
points = [item['point'] for item in tsne_data]
paths = [item['path'] for item in tsne_data]

# Convert points to numpy array
tsne_array = np.array(points)

# Define parameter range for eps
eps_range = np.arange(0.1, 25, 0.1)

# Initialize variables to store the best parameters and their corresponding results
best_eps = None
min_samples = 5
max_clusters = 0
min_noise = float('inf')
best_labels = None

# Iterate over the eps range
for eps in eps_range:
    # Apply DBSCAN with current eps and fixed min_samples
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')
    labels = dbscan.fit_predict(tsne_array)

    # Number of clusters found (excluding noise points labeled as -1)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    # Number of noise points
    n_noise = list(labels).count(-1)

    # Check if this is the best parameter combination so far
    if n_noise < 5 and (n_clusters > max_clusters or (n_clusters == max_clusters and n_noise < min_noise)):
        best_eps = eps
        max_clusters = n_clusters
        min_noise = n_noise
        best_labels = labels

# Print the best eps and corresponding results
print(f"Best eps: {best_eps}")
print(f"Fixed min_samples: {min_samples}")
print(f"Maximum number of clusters: {max_clusters}")
print(f"Minimum number of noise points: {min_noise}")

# Append the cluster labels to the original data
for item, label in zip(tsne_data, best_labels):
    item['cluster'] = int(label)

# Save the updated data to a new JSON file
with open('tsne_results_with_clusters(DBSCAN).json', 'w') as file:
    json.dump(tsne_data, file, indent=4)

# Create a DataFrame with the best results for visualization
df = pd.DataFrame(tsne_array, columns=['x', 'y'])
df['cluster'] = best_labels
df['path'] = paths

# Print the number of points in each cluster
cluster_counts = df['cluster'].value_counts().sort_index()
print("Number of points in each cluster:")
print(cluster_counts)

# Define a path effect for text background
stroke = withStroke(linewidth=2, foreground='white')

# Plot the best clusters
plt.figure(figsize=(10, 7))
scatter = plt.scatter(df['x'], df['y'], c=df['cluster'], cmap='turbo', s=50, alpha=0.5, label='Clusters')
plt.scatter(df[df['cluster'] == -1]['x'], df[df['cluster'] == -1]['y'], color='black', marker='x', s=50, label='Noise')
plt.title(f'DBSCAN Clustering of t-SNE Results (eps={round(best_eps, 3)}, min_samples={min_samples})')
plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.xticks([])
plt.yticks([])

# Annotate clusters with cluster number and number of points
for cluster_num, count in cluster_counts.items():
    if cluster_num != -1:  # Exclude noise points
        cluster_points = df[df['cluster'] == cluster_num]
        mean_x = cluster_points['x'].mean()
        mean_y = cluster_points['y'].mean()
        plt.annotate(f'Cluster {cluster_num}\n({count} points)',
                     xy=(mean_x, mean_y), xytext=(5,5),
                     textcoords='offset points', fontsize=9, ha='center',
                     path_effects=[stroke])

if '-1' in df['cluster'].astype(str).values:
    plt.legend()

plt.show()
