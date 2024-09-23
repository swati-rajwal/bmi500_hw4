import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import os

# Specify the folder name or path
output_folder = 'output'

# Create the folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Folder '{output_folder}' created.")
else:
    print(f"Folder '{output_folder}' already exists.")


df = pd.read_csv('data/geyser.csv')
print("\nReading the dataset (which has been manually updated for 7 rows- please see the table 1 of report)....")
print(f"\n####### Shape of dataset: {df.shape} ######")
print("\n######## Sample dataset entries #######")
print(df.sample(4))

duplicates = df.duplicated()
if duplicates.any():
    print(f"\n###### Number of duplicate rows: {duplicates.sum()} #####")
    print(df[duplicates]) 
    print("\n### Please note that although there were duplicate entries, I did not remove duplicate rows from the dataset as the repetition of eruption time and waiting time could represent actual recurring events in the data that might be reflecting the natural variability of the geyser's behavior rather than data entry errors. Removing duplicates may unintentionally discard valid observations.")
else:
    print("\nNo duplicate rows found.")

# Summary Statistics
summary_stats = df.describe()
print("\n######## Summary Statistics #########")
print(summary_stats)

# Missing Values Check
missing_values = df.isnull().sum()
print("\n####### Missing Values ########")
print(missing_values)

# Dataframe distribution (After manual updation and outlier removal)
fig, axs = plt.subplots(2, 1, figsize=(10, 8))
mean_eruptions = df['eruptions'].mean()
median_eruptions = df['eruptions'].median()
axs[0].boxplot(df['eruptions'], vert=False, patch_artist=True, 
               boxprops=dict(linewidth=1.7),
               whiskerprops=dict(linewidth=1.7),
               capprops=dict(linewidth=1.7), 
               medianprops=dict(linewidth=1.7))
axs[0].text(-0.09, 0.7, '(A)', transform=axs[0].transAxes, fontsize=14, fontweight='bold', va='center')
axs[0].set_xlabel('Duration of Eruptions (minutes)', fontsize=14)
# axs[0].set_ylabel('Distribution', fontsize=14)
axs[0].grid(True)
axs[0].annotate(f'Mean: {mean_eruptions:.2f}\nMedian: {median_eruptions:.2f}',
                xy=(0.8, 0.8), xycoords='axes fraction', fontsize=12,
                bbox=dict(facecolor='white', alpha=0.5))

mean_waiting = df['waiting'].mean()
median_waiting = df['waiting'].median()
axs[1].boxplot(df['waiting'], vert=False, patch_artist=True, 
               boxprops=dict(linewidth=1.7),  
               whiskerprops=dict(linewidth=1.7),
               capprops=dict(linewidth=1.7),  
               medianprops=dict(linewidth=1.7))
axs[1].text(-0.09, 0.7, '(B)', transform=axs[1].transAxes, fontsize=14, fontweight='bold', va='center')
axs[1].set_xlabel('Waiting Time (minutes)', fontsize=14)
# axs[1].set_ylabel('Distribution', fontsize=14)
axs[1].grid(True)
axs[1].annotate(f'Mean: {mean_waiting:.2f}\nMedian: {median_waiting:.2f}',
                xy=(0.8, 0.8), xycoords='axes fraction', fontsize=12,
                bbox=dict(facecolor='white', alpha=0.5))

plt.tight_layout()
# plt.show()
plt.subplots_adjust(hspace=0.4)
plt.savefig('output/outlier_removed_distribution_new.png')
print("\nDataset distribution after outlier removal image saved! Please check the 'output/' folder")
plt.close()

# A Bad Plot Example
plt.figure(figsize=(5,5))  # Unusual and awkward figure size
plt.scatter(df['eruptions'], df['waiting'], color='red')  # Scatterplot without seaborn, and color makes it harder to interpret
plt.title('')
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.savefig("output/bad_figure.png")
print("\nScatter plot saved! Please check the 'output/' folder.....")
plt.close()

# sample Good plot
corr, p_val = pearsonr(df['eruptions'], df['waiting'])
print(f"Pearson Correlation Coefficient: {corr:.4f}")
if (p_val<0.05):
    print(f"P-value is {p_val} which is <0.05")
    
# scatter plot with a regression line
plt.figure(figsize=(10, 6))
sns.regplot(x='eruptions', y='waiting', data=df, scatter_kws={'s': 50, 'alpha': 0.7}, line_kws={'color': 'red'}, ci=None)
plt.xlabel('Eruptions Duration (minutes)', fontsize=14)
plt.ylabel('Waiting Time (minutes)', fontsize=14)
plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.7)
plt.minorticks_on()
plt.tick_params(which='both', width=1)
plt.tick_params(which='minor', length=4, color='gray')
# plt.show()
plt.savefig('output/correlation_plot.png')
print("\nA good scatter plot saved! Please check the 'output/' folder...")
plt.close()

print("\nCODE EXECUTION COMPLETED. Terminal output has been stored in the 'output/output.txt' file as well for future reference.\n")