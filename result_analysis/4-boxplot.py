import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('expDuration.csv')

# color for B2, B1, A2, A1
custom_colors = ['#dcb0f2', '#f89c74', '#f6cf71', '#66c5cc']
alpha_box = 0.7  

# Ensure the length of custom_colors matches the number of configurations
assert len(custom_colors) == len(data['Configuration'].unique()), "Color array length must match the number of configurations"

# Get sorted unique configuration names in descending order: A1 A2 B1 B2
sorted_configs = sorted(data['Configuration'].unique(), reverse=True)

# Sort the dataframe by Configuration in descending order
data_sorted = data.sort_values('Configuration', ascending=False)

# Create a figure and axis
plt.figure(figsize=(12, 8))
ax = plt.gca()

# Create a box plot
boxplot = ax.boxplot(
    [data_sorted[data_sorted['Configuration'] == config]['Total'] for config in sorted_configs],
    tick_labels=sorted_configs, 
    patch_artist=True,
    vert=False,  # Horizontal box plot
    widths=0.2 
)

# Apply custom colors with alpha to the boxplot
for patch, color in zip(boxplot['boxes'], custom_colors):
    patch.set_facecolor(color)
    patch.set_alpha(alpha_box)  # Set alpha for the box color

for i, config in enumerate(sorted_configs):
    config_data = data_sorted[data_sorted['Configuration'] == config]['Total']
    # Calculate y-values with offset
    y = [i + 1] * len(config_data)
    # Plot each data point in the configuration with corresponding color
    ax.scatter(config_data, y, color=custom_colors[i], alpha=0.6, edgecolor='black', s=50, label=f'Data points - {config}')

# Calculate statistics for each configuration
statistics = data_sorted.groupby('Configuration')['Total'].describe()

# Function to calculate outliers
def get_outliers(data, q1, q3):
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return data[(data < lower_bound) | (data > upper_bound)]

# Create lists for legend handles and labels
handles = []
labels = []

threshold_handle = plt.Line2D([0], [0], color='grey', linestyle='--', linewidth=1, label='Temporal Length')
handles.append(threshold_handle)

for i, config in enumerate(sorted_configs):
    stats = statistics.loc[config]
    q1 = stats['25%']
    q3 = stats['75%']
    min_val = stats['min']
    max_val = stats['max']
    median = stats['50%']
    mean_including = stats['mean']

    # Get the data for this configuration
    config_data = data_sorted[data_sorted['Configuration'] == config]['Total']

    # Get outliers
    outliers = get_outliers(config_data, q1, q3)

    # Calculate the mean excluding outliers
    config_data_no_outliers = config_data[~config_data.isin(outliers)]
    mean_excluding = config_data_no_outliers.mean()

    # Calculate the maximum excluding outliers
    max_excluding = config_data_no_outliers.max()
    min_excluding = config_data_no_outliers.min()

    # Position on the y-axis
    y_pos = i + 1

    # annoate min value
    plt.text(
        min_excluding, y_pos - 0.25,
        f'{min_val:.2f}',
        fontsize=12,
        verticalalignment='bottom',
        horizontalalignment='center'
    )

    # annotate max value
    plt.text(
        max_excluding, y_pos - 0.25,
        f'{max_excluding:.2f}',
        fontsize=12,
        verticalalignment='bottom',
        horizontalalignment='center'
    )

    # annoate any existing outliers
    if not outliers.empty:
        for outlier in outliers:
            ax.scatter(outlier, y_pos, color=custom_colors[i], marker="o", zorder=5)
            plt.text(
                outlier, y_pos + 0.1,
                f'{outlier:.2f}',
                fontsize=12,
                color='black',
                verticalalignment='bottom',
                horizontalalignment='center'
            )

    # plot the mean value
    ax.scatter(mean_excluding, y_pos, color='black', marker="+", zorder=5)

    # annotate mean value
    plt.text(
        mean_excluding, y_pos - 0.3,
        f'Mean: {mean_excluding:.2f}',
        fontsize=12,
        color='black',
        verticalalignment='bottom',
        horizontalalignment='center'
    )
    
    # annotate median value
    plt.text(
        median, y_pos + 0.25,
        f'Median: {median:.2f}',
        fontsize=12,
        color='black',
        verticalalignment='top',
        horizontalalignment='center'
    )

# Set labels and title
ax.set_xlabel('Experience Duration (in minute)', fontsize=12)
ax.set_ylabel('Configuration', fontsize=12)

# Add a vertical dotted line at value 12.5
ax.axvline(x=12.5, color='grey', linestyle='--', linewidth=1, label='Temporal Length')

# Add the legend to the plot
ax.legend(handles=handles, loc='best', fontsize=12)

# Show the plot
plt.show()
