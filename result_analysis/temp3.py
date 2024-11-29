import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('dwell.csv')

# Create the scatter plot
plt.figure(figsize=(10, 6))
for config in df['Configuration'].unique():
    subset = df[df['Configuration'] == config]
    plt.scatter(subset['Participant'], subset['Mean'], label=f'Config {config}', alpha=0.7)

# Add labels and title
plt.xlabel('Participant')
plt.ylabel('Mean')
plt.title('Scatter Plot of Mean Values by Configuration')
plt.legend()
plt.grid(True)
plt.show()
