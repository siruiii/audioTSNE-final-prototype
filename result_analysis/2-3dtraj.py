import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

file_path = '../console_log/2-A1-merge.json'
filename = file_path.split('/')[-1]
config = filename.split('-')[1]

with open(file_path, 'r') as file:
    data = json.load(file)

x_coords = np.array([-item["point3d"][0] for item in data])
y_coords = np.array([item["point3d"][2] for item in data])
z_coords = np.array([item["point3d"][1] for item in data])
clusters = np.array([item["Cluster"] for item in data])
unique_clusters = np.unique(clusters)

cluster_colors = {0: '#9468B8', 1: '#0079B1', 2: '#23A03A',  3: '#FF7C27'}

if (config == 'A1'):
    cluster_handlers = {-1: "noise", 0: "Singing", 1: "Oral Narrative, Clapping", 2: "Instrumental Music 1", 3: "Instrumental Music 2"}
elif (config == 'A2'):
    cluster_handlers = {-1: "noise", 0: "Clapping", 1: "Singing(female & male)", 2: "Singing(female)", 3: "Oral Narrative"}
elif (config == 'B1'):
    cluster_handlers = {-1: "noise", 0: "Singing", 1: "Reciting"}
elif (config == 'B2'):
    cluster_handlers = {-1: "noise", 0: "Reciting", 1: "Singing"}

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
previous_color= None

for i, cluster in enumerate(clusters):
    if cluster == -1:
        color = previous_color 
    else:
        color = cluster_colors[cluster]
        previous_color = color
    ax.plot(x_coords[i:i+2], y_coords[i:i+2], z_coords[i:i+2], color=color) 
    ax.scatter(x_coords[i:i+2], y_coords[i:i+2],z_coords[i:i+2], color=color, s=20)  

handles = [plt.Rectangle((0, 0), 1, 1, color=cluster_colors[cluster]) for cluster in unique_clusters if cluster != -1]
#plt.legend(handles, [f'{cluster_handlers[cluster]}' for cluster in unique_clusters if cluster != -1], fontsize=15)
#plt.grid(True)
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
plt.show()
