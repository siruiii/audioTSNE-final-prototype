import json
import matplotlib.pyplot as plt

# Read JSON data from a file
with open('A2with2D.json', 'r') as file:
    data = json.load(file)

# Extract id and sequence from the data
ids = []
sequences = []

for entry in data:
    path = entry["Path"]
    id = int(path.split('/').pop().split('_')[0])-75
    ids.append(id)
    sequences.append(entry["Sequence"])

# Combine id and sequence into a list of tuples and sort by id
sorted_data = sorted(zip(ids, sequences))

# Unzip sorted data
sorted_ids, sorted_sequences = zip(*sorted_data)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(sorted_ids, sorted_sequences, marker='o', linestyle='-')
plt.xlabel('Audio Index')
plt.ylabel('Sequence')
plt.title('Plot of Sequence vs ID')
plt.grid(True)
plt.show()
