import json
import matplotlib.pyplot as plt

# Specify the path to your JSON file here
json_file_path = '../audio_processing/meshrep+peking_tsne_results.json'  # Change this to your JSON file path if it's different

# Load data from the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract points and labels
points = [d["point"] for d in data]
labels = [d["path"].split('/')[-1].split('_')[0] for d in data]

# Unzip points into x and y coordinates
y_coords, x_coords = zip(*points)
x_coords = [15 * x for x in x_coords]
y_coords = [15 * y for y in y_coords]

# Create a scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(x_coords, y_coords, color='blue')

# Add labels
for i, label in enumerate(labels):
    plt.text(x_coords[i], y_coords[i], label, fontsize=12, ha='right')

# Set titles and labels
plt.title('Scatter Plot of Points')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.show()
