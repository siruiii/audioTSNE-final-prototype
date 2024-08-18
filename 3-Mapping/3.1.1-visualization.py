import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the JSON file
with open('../3-Mapping/meshrep25-5sec_coordinates.json', 'r') as file:
    data = json.load(file)

# Extract 3D points
points_3d = [entry["point3d"] for entry in data]

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot for all points
for point in points_3d:
    ax.scatter(-point[0], point[2], point[1], color='b')

# Labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Points Visualization')

# Display the plot
plt.show()
