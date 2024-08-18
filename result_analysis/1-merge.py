import pandas as pd
import json
import math

# Read file 1
with open('../console_log/A1-console.json', 'r') as f:
    file1_data = json.load(f)

# Read file 2
with open('../3-Mapping/meshrep25-5sec_coordinates.json', 'r') as f:
    file2_data = json.load(f)

# Create DataFrames
df1 = pd.DataFrame(file1_data)
df2 = pd.DataFrame(file2_data)
df2.rename(columns={'path': 'Path'}, inplace=True)
df2.rename(columns={'point': '2D_Coord'}, inplace=True)
df2.rename(columns={'cluster': 'Cluster'}, inplace=True)
df_combined = pd.merge(df1, df2, on='Path', how='left')

# Convert DataFrame to dictionary
result_dict = df_combined.to_dict(orient='records')

# Save combined DataFrame to JSON
with open('merge_result1.json', 'w') as file:
    json.dump(result_dict, file, indent=4)