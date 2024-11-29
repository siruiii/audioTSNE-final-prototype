import json
import matplotlib.pyplot as plt

# Read JSON data from a file
with open('../console_log/2-A1-merge.json', 'r') as file:
    data = json.load(file)

# Extract id and sequence from the data
ids = []
sequences = []

for entry in data:
    path = entry["Path"]
    id = int(path.split('/').pop().split('_')[0])
    ids.append(id)
    sequences.append(entry["Sequence"])

# Combine id and sequence into a list of tuples and sort by sequence
sorted_data = sorted(zip(sequences, ids))

# Unzip sorted data
sorted_sequences, sorted_ids = zip(*sorted_data)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(sorted_sequences, sorted_ids, marker='o', linestyle='-',color="#66c5cc")  # Plot by sequence order
plt.xlabel('Spatial Exploration Sequence')
plt.ylabel('Temporal Sequence')
plt.show()
