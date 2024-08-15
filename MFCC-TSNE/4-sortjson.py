import json

def sort_json_file(input_file, output_file):
    # Read the JSON data from the input file
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Sort the data by the second element in the 'point' array
    sorted_data = sorted(data, key=lambda x: x['point'][1])
    
    # Write the sorted data to the output file
    with open(output_file, 'w') as file:
        json.dump(sorted_data, file, indent=4)

# Example usage
input_file = '../meshrep5sec_tsne_results.json'
output_file = '../meshrep5sec_tsne_results_sorted.json'
sort_json_file(input_file, output_file)
