import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

def format_demographics(df, continuous_vars, categorical_vars):
    results_list = []
    
    # Process each continuous variable
    for var in continuous_vars:
        stats = df[var].agg(['mean', 'std', 'min', 'max'])
        stats = stats.fillna("")  # Replace NaNs with empty strings
        missing_count = df[var].isna().sum()
        total_count = len(df[var])
        missing_percentage = (missing_count / total_count * 100) if total_count > 0 else 0
        row_df = pd.DataFrame({
            'Variable': [f"**{var}, mean (SD)**"],
            'Overall': [f"{stats['mean']:.2f} ({stats['std']:.2f})" if pd.notna(stats['mean']) else ""],
            'Min': [f"{stats['min']:.2f}" if stats['min'] != "" else ""],
            'Max': [f"{stats['max']:.2f}" if stats['max'] != "" else ""],
            'Missing (%)': [f"{missing_count} ({missing_percentage:.2f}%)"]
        })
        results_list.append(row_df)
    
    # Process each categorical variable
    for var in categorical_vars:
        non_na_count = df[var].dropna().value_counts()
        total = non_na_count.sum()
        percentages = (non_na_count / total * 100).round(2) if total > 0 else pd.Series()
        missing_count = df[var].isna().sum()
        total_count = len(df[var])
        missing_percentage = (missing_count / total_count * 100) if total_count > 0 else 0
        
        main_row_df = pd.DataFrame({
            'Variable': [f"**{var}**"],  # Bold main categories
            'Overall': [""],
            'Min': [""],
            'Max': [""],
            'Missing (%)': [f"{missing_count} ({missing_percentage:.2f}%)"]
        })
        results_list.append(main_row_df)

        # Process non-missing categories, use plain text with extra spaces for "indentation"
        for category, count in non_na_count.items():
            sub_row_df = pd.DataFrame({
                'Variable': [f"    {category}, n (%)"],  # Attempting to use spaces for indentation
                'Overall': [f"{count} ({percentages[category]}%)"],
                'Min': [""],
                'Max': [""],
                'Missing (%)': [""]
            })
            results_list.append(sub_row_df)

    # Concatenate all result rows into a single DataFrame
    results_df = pd.concat(results_list).set_index('Variable')
    return results_df

def plot_violin(df, x_var, y_var,title='', y_label= ''):
    
    sns.set(style="darkgrid")  # This sets a white background with grid lines
    plt.figure(figsize=(6, 4))
    sns.violinplot(x=x_var, y=y_var, data=df, cut=0, bw='scott',  # Using 'scott' automatic bandwidth
                   kde_kws={"bw_adjust": 1.5}, palette="Set3")  # Adjusted bandwidth for smoothing, Set3 palette
    plt.ylabel(y_label)
    plt.xlabel('')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.xticks(rotation=45, fontsize=10)  # Smaller font size for x-ticks
    plt.yticks(fontsize=10)  # Smaller font size for y-ticks

    # Adjust y-axis limits if necessary
    data_min = df[y_var].min()
    data_max = df[y_var].max()
    y_buffer = (data_max - data_min) * 0.1  # Adding 10% buffer on both ends
    plt.ylim(data_min - y_buffer, data_max + y_buffer)

    plt.show()











