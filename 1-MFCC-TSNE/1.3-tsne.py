import json
import numpy as np
import os
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Load features from JSON file
def load_features(json_path):
    with open(json_path, 'r') as f:
        features_list = json.load(f)
    return features_list

# Run t-SNE on the features
def run_tsne(features_list):
    # Extract features and file paths
    features = np.array([item['features'] for item in features_list])
    file_paths = [item['file'] for item in features_list]

    # Initialize t-SNE
    tsne = TSNE(n_components=2, learning_rate=300, perplexity=50, verbose=2, angle=0.1)
    tsne_results = tsne.fit_transform(features)
    
    # Prepare results in the desired format
    results = [{'path': os.path.relpath(path), 'point': point.tolist()} for path, point in zip(file_paths, tsne_results)]
    
    return results, tsne_results, file_paths

# Save t-SNE results to JSON file
def save_tsne_results(results, output_json_path):
    with open(output_json_path, 'w') as f:
        json.dump(results, f, indent=4)

# Visualize t-SNE results
def visualize_tsne(tsne_results, file_paths):
    plt.figure(figsize=(10, 8))

    # Get unique subfolders and assign a color to each
    subfolders = [os.path.basename(os.path.dirname(path)) for path in file_paths]
    unique_subfolders = list(set(subfolders))
    cmap = plt.get_cmap('tab10', len(unique_subfolders))  # Use 'tab10' colormap with as many colors as there are subfolders
    color_dict = {subfolder: cmap(i) for i, subfolder in enumerate(unique_subfolders)}

    # Plot each point with the color corresponding to its subfolder
    for subfolder in unique_subfolders:
        indices = [i for i, folder in enumerate(subfolders) if folder == subfolder]
        points = tsne_results[indices]
        plt.scatter(points[:, 0], points[:, 1], s=10, alpha=0.7, color=color_dict[subfolder], label=subfolder)

    plt.title('t-SNE Visualization of Audio Features')
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    plt.legend()
    plt.show()

# Example usage
features_json_path = 'peking25-10sec_features.json'
tsne_results_json_path = 'peking25-10sec_tsne_results1.json'

# Load features and run t-SNE
features_list = load_features(features_json_path)
tsne_results, tsne_coordinates, file_paths = run_tsne(features_list)

# Save t-SNE results
save_tsne_results(tsne_results, tsne_results_json_path)

# Visualize t-SNE results
visualize_tsne(tsne_coordinates, file_paths)
