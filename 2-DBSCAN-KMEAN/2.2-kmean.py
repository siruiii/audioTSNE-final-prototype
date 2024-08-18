import json
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
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

# Create a DataFrame with the best results for visualization
df = pd.DataFrame(tsne_array, columns=['x', 'y'])
df['cluster'] = best_labels
df['path'] = paths

# Print the number of points in each cluster
cluster_counts = df['cluster'].value_counts().sort_index()
print("Number of points in each cluster:")
print(cluster_counts)

# Find the largest cluster
largest_cluster = cluster_counts.idxmax()
largest_cluster_size = cluster_counts.max()
average_cluster_size = cluster_counts.mean()
print(f"Largest cluster: {largest_cluster} with size {largest_cluster_size}")

# Calculate the number of splits based on average size
num_splits = max(2, int(np.ceil(largest_cluster_size / average_cluster_size)))
print(f"Number of splits for the largest cluster: {num_splits}")

# Extract points from the largest cluster
largest_cluster_indices = np.where(best_labels == largest_cluster)[0]
largest_cluster_points = tsne_array[largest_cluster_indices]

# Apply K-means to further split the largest cluster
kmeans = KMeans(n_clusters=num_splits, random_state=0)
kmeans_labels = kmeans.fit_predict(largest_cluster_points)

# Update labels for the largest cluster only
new_labels = best_labels.copy()
for idx, cluster_idx in zip(largest_cluster_indices, kmeans_labels):
    new_labels[idx] = max(best_labels) + 1 + cluster_idx  # Shift new cluster labels

# Update the cluster counts
df['cluster'] = new_labels
new_cluster_counts = df['cluster'].value_counts().sort_index()
print("Updated number of points in each cluster:")
print(new_cluster_counts)

stroke = withStroke(linewidth=2, foreground='white')

# Plot the best clusters
plt.figure(figsize=(10, 7))
scatter = plt.scatter(df['x'], df['y'], c=df['cluster'], cmap='turbo', s=50, alpha=0.5, label='Clusters')
plt.scatter(df[df['cluster'] == -1]['x'], df[df['cluster'] == -1]['y'], color='black', marker='x', s=50, label='Noise')
plt.title(f'DBSCAN with KMEAN Clustering of t-SNE Results')
plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.xticks([])
plt.yticks([])

# Annotate clusters with cluster number and number of points
for cluster_id in new_cluster_counts.index:
        cluster_points = df[df['cluster'] == cluster_id]
        mean_x = cluster_points['x'].mean()
        mean_y = cluster_points['y'].mean()
        if cluster_id == -1:
            continue  # Skip noise points for labeling
        num_points = new_cluster_counts[cluster_id]
        plt.annotate(f'Cluster {cluster_id}\n({num_points} points)',
                     xy=(mean_x, mean_y), xytext=(5,5),
                     textcoords='offset points', fontsize=9, ha='center',
                     path_effects=[stroke])

if '-1' in df['cluster'].astype(str).values:
    plt.legend()

plt.show()

# Update tsne_data with the new labels
for i, item in enumerate(tsne_data):
    item['cluster'] = int(new_labels[i])  # Convert to native Python int

# Save the updated data to a new JSON file
with open('tsne_results_with_clusters(DBSCAN with KMEAN).json', 'w') as file:
    json.dump(tsne_data, file, indent=4)
