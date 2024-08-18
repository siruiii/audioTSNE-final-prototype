import json
import numpy as np
import matplotlib.pyplot as plt

# Load JSON data from a file
file_path = 'merge_result1.json'  # Replace with the path to your JSON file

with open(file_path, 'r') as file:
    data = json.load(file)

# Extract 3D points
points_3d = [np.array(item['point3d']) for item in data]

# Calculate distances between consecutive points
distances = []
for i in range(len(points_3d) - 1):
    distance = np.linalg.norm(points_3d[i + 1] - points_3d[i])
    distances.append(distance)

# Print distances in their original order
print("Distances between consecutive points:")
for i, distance in enumerate(distances):
    print(f"Distance {i + 1}: {distance}")

# Plot distances as a line plot
plt.plot(distances, marker='o', linestyle='-', color='black', label='Distances')

# Add title, labels, legend, and grid
plt.title('Distances Between Consecutive 3D Points')
plt.xlabel('Sequence')
plt.ylabel('Distance')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()