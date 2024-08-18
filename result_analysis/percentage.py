import json

# Path to your JSON file
json_file_path = 'B1with2D.json'

# Read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Initialize an empty set to store unique IDs
unique_ids = set()

# Iterate through each item in the JSON data
for item in data:
    path = item["Path"]
    # Extract ID from path
    id = int(path.split('/').pop().split('_')[0])
    # Add ID to the set
    unique_ids.add(id)
    # print(id)

# The number of distinct IDs
num_distinct_ids = len(unique_ids)
print(f'Number of distinct IDs: {num_distinct_ids}')
