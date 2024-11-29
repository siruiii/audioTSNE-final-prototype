import json
import numpy as np
import matplotlib.pyplot as plt

# File paths
file_paths = [
    '../console_log/1-A2-merge.json'
]

# Cluster color mapping


# Define colors for each line corresponding to each file
# A1, A2, B1, B2
#line_colors = ['#66c5cc', '#f6cf71','#f89c74', '#dcb0f2' ]  # Add more colors if there are more files
# B1, B2
#line_colors = ['#f89c74', '#dcb0f2' ]
#line_colors = ['#dcb0f2' ]
# A2, B2
line_colors = ['#f6cf71','#dcb0f2' ]
# A1, B1
#line_colors = ['#66c5cc', '#f89c74']
# A1, A2
#line_colors = ['#66c5cc', '#f6cf71']
# Create a figure and axis for combined plotting
plt.figure(figsize=(16, 2))
ax = plt.gca()

# Loop over each file path
for i, file_path in enumerate(file_paths):
    # Extract the filename and tester information
    filename = file_path.split('/')[-1]
    tester = filename.split('-')[0]  # Extracts tester information

    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Sort the data by 'Sequence' to ensure proper accumulation over time
    data_sorted = sorted(data, key=lambda x: x['Sequence'])

    # Prepare data for plotting
    sequences = [entry['Sequence'] for entry in data_sorted]
    durations = [entry['Duration'] for entry in data_sorted]
    clusters = [entry['Cluster'] for entry in data_sorted]
    label=["Meshrep 10-sec", "Peking Opera 10-sec"]

    # Calculate cumulative dwell time
    cumulative_dwell_time = np.cumsum(durations)

    # Find the first non-zero point to connect from (0,0)
    if len(cumulative_dwell_time) > 0:
        first_time = cumulative_dwell_time[0]
        first_duration = durations[0]

        ax.plot(
            cumulative_dwell_time,
            durations,
            marker='o',
            linestyle='-',
            label=f'{label[i]}',
            color=line_colors[i], 
            markerfacecolor='none',
            markersize=2
        )
        ax.scatter(
            0,
            0,
            c=line_colors[i],  
            marker='o',           
            s=2,                
        )

        ax.plot(
            [0, first_time],
            [0, first_duration],
            color=line_colors[i], 
            linestyle='-'     
        )

# Add labels and legend
plt.xlabel('Time (in sec)', fontsize=12)
plt.ylabel('Dwell Time\n (in sec)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.xticks([0,60,120], fontsize=10)
plt.yticks([0,5,10], fontsize=10)
plt.show()
