import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# Load features from JSON file
def load_features(json_path):
    with open(json_path, 'r') as f:
        features_list = json.load(f)
    return features_list

# Compute the similarity matrix
def compute_similarity_matrix(features_list):
    # Extract features
    features = np.array([item['features'] for item in features_list])
    
    # Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(features)
    
    return similarity_matrix

# Visualize the similarity matrix
def visualize_similarity_matrix(similarity_matrix, output_image_path):
    plt.figure(figsize=(10, 8))
    sns.heatmap(similarity_matrix, cmap='winter', annot=False, fmt=".2f")
    plt.title('Similarity Matrix Heatmap')
    plt.xlabel('Audio Files')
    plt.ylabel('Audio Files')
    plt.savefig(output_image_path)
    plt.show()

# Example usage
features_json_path = 'meshrep25-10sec_features.json'
similarity_matrix_image_path = 'meshrep25-5sec_features_similarity_matrix.png'

# Load features and compute similarity matrix
features_list = load_features(features_json_path)
similarity_matrix = compute_similarity_matrix(features_list)

# Visualize the similarity matrix
visualize_similarity_matrix(similarity_matrix, similarity_matrix_image_path)
