import json
import matplotlib.pyplot as plt


json_file_path = 'split0015443.json' 
with open(json_file_path, 'r') as file:
    data = json.load(file)


points = [d["point"] for d in data]

x_coords, y_coords = zip(*points)
x_coords = [x for x in x_coords]
y_coords = [y for y in y_coords]


plt.figure(figsize=(10, 7))
plt.scatter(x_coords, y_coords, color='#778899', s=50) 

# Add labels
# for i, label in enumerate(labels):
#     plt.text(x_coords[i], y_coords[i], label, fontsize=7, ha='center', va='center')  # Center the labels

# Set titles and labels
# plt.title('2D Visualization of t-SNE Results')
plt.xticks([])
plt.yticks([])
plt.xlabel('t-SNE Dimension 1', fontsize=15)
plt.ylabel('t-SNE Dimension 2', fontsize=15)
plt.show()
