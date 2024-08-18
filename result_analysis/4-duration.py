import json
import matplotlib.pyplot as plt

# Load data from JSON file
with open('merge_result1.json', 'r') as file:
    data = json.load(file)

# Extracting data for plotting
sequences = [entry["Sequence"] for entry in data]
durations = [entry["Duration"] for entry in data]

# Creating the histogram
plt.figure(figsize=(10, 6))
plt.bar(sequences, durations, color='skyblue', edgecolor='black')
plt.xlabel('Sequence')
plt.ylabel('Duration')
plt.title('Duration by Sequence')
plt.xticks(sequences)  # Ensure that all sequence values are shown on the x-axis
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.show()
