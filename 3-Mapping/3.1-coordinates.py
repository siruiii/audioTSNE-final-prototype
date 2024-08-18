import json
import math

# Function to process the JSON data
def process_json_data(data):
    # Compute the min and max for normalization
    points = [item['point'][0]*1.3 for item in data]
    max_x = max(points)
    min_x = min(points)
    range_x = max_x - min_x
    radius = 150
    print(max_x,min_x,range_x)

    # Add the 3d field to each item
    for item in data:
        point = item['point']
        x2d = point[0]*1.3
        y3d = point[1]*1.3
        theta = ((x2d - min_x) / range_x) * 2 * math.pi
        x3d = radius * math.cos(theta)
        z3d = radius * math.sin(theta)
        item['point3d'] = [x3d, y3d, z3d]
    
    return data

# Read JSON data from a file
input_file = '../2-DBSCAN-KMEAN/peking25-10sec_tsne_results_with_clusters(DBSCAN).json'  # Replace with your input file path
output_file = '_coordinates.json'  # Replace with your output file path

with open(input_file, 'r') as file:
    data = json.load(file)

# Process the JSON data
processed_data = process_json_data(data)

# Save the updated JSON data to a file
with open(output_file, 'w') as file:
    json.dump(processed_data, file, indent=2)

print(f'Processed data saved to {output_file}')
