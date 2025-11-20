import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import argparse

def generate_energy_usage_plots(csv_file_path, output_dir='plots'):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: Input CSV file '{csv_file_path}' not found.")
        return

    # Combine date/time columns into a single datetime object
    df['Timestamp'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']])

    # --- Plot 1: Average Energy Usage by Hour of Day (Line Plot) ---
    print("Generating plot: Average Energy Usage by Hour of Day...")
    hourly_avg = df.groupby('Hour')['Energy_Consumption_kWH'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Hour', y='Energy_Consumption_kWH', data=hourly_avg)
    plt.title('Average Energy Usage by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Energy Consumption (kWH)')
    plt.grid(True)
    plot1_path = os.path.join(output_dir, 'average_usage_by_hour.png')
    plt.savefig(plot1_path)
    plt.close() # Close the plot to free memory
    print(f"Saved plot to {plot1_path}")

    # --- Plot 2: Heatmap of Average Energy Usage by Hour and Day of Week ---
    print("Generating plot: Heatmap of Average Energy Usage by Hour and Day of Week...")
    df['DayOfWeek'] = df['Timestamp'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['DayOfWeek'] = pd.Categorical(df['DayOfWeek'], categories=day_order, ordered=True)

    # Add observed=False to groupby to silence FutureWarning
    pivot_table = df.pivot_table(values='Energy_Consumption_kWH', index='Hour', columns='DayOfWeek', aggfunc='mean', observed=False)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, cmap='viridis', annot=True, fmt=".1f", linewidths=.5)
    plt.title('Average Energy Usage by Hour and Day of Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Hour of Day')
    plot2_path = os.path.join(output_dir, 'heatmap_usage_by_hour_day.png')
    plt.savefig(plot2_path)
    plt.close() # Close the plot to free memory
    print(f"Saved plot to {plot2_path}")

    # --- Plot 3: Daily Usage Profile by Day of Week (Multi-line Plot) ---
    print("Generating plot: Daily Usage Profile by Day of Week...")
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df, x='Hour', y='Energy_Consumption_kWH', hue='DayOfWeek', errorbar=None, palette='tab10')
    plt.title('Average Daily Energy Usage Profile by Day of Week')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Energy Consumption (kWH)')
    plt.xticks(range(0, 24)) # Ensure all hours are shown
    plt.grid(True)
    plt.legend(title='Day of Week', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plot3_path = os.path.join(output_dir, 'daily_profile_by_day_of_week.png')
    plt.savefig(plot3_path)
    plt.close()
    print(f"Saved plot to {plot3_path}")

    # --- Plot 4: Monthly/Seasonal Usage Trends (Bar Plot) ---
    print("Generating plot: Monthly/Seasonal Usage Trends...")
    monthly_avg = df.groupby('Month')['Energy_Consumption_kWH'].mean().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Month', y='Energy_Consumption_kWH', data=monthly_avg, palette='viridis', hue='Month', legend=False)
    plt.title('Average Monthly Energy Usage Trends')
    plt.xlabel('Month')
    plt.ylabel('Average Energy Consumption (kWH)')
    plt.xticks(range(0, 12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.grid(axis='y')
    plot4_path = os.path.join(output_dir, 'monthly_usage_trends.png')
    plt.savefig(plot4_path)
    plt.close()
    print(f"Saved plot to {plot4_path}")

    # --- Plot 5: Distribution of Consumption Values (Histogram) ---
    print("Generating plot: Distribution of Consumption Values...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Energy_Consumption_kWH'], bins=50, kde=True, color='skyblue')
    plt.title('Distribution of Energy Consumption Values')
    plt.xlabel('Energy Consumption (kWH)')
    plt.ylabel('Frequency')
    plt.grid(axis='y')
    plot5_path = os.path.join(output_dir, 'consumption_distribution.png')
    plt.savefig(plot5_path)
    plt.close()
    print(f"Saved plot to {plot5_path}")

    # --- Plot 6: Top 10 Peak Usage Hours/Days (Bar Chart) ---
    print("Generating plot: Top 10 Peak Usage Hours/Days...")
    df['Day_Hour'] = df['DayOfWeek'].astype(str) + ' - ' + df['Hour'].astype(str).str.zfill(2) + ':00'
    peak_usage = df.groupby('Day_Hour')['Energy_Consumption_kWH'].mean().nlargest(10).reset_index()
    
    plt.figure(figsize=(12, 7))
    sns.barplot(x='Energy_Consumption_kWH', y='Day_Hour', data=peak_usage, palette='Reds_d', hue='Day_Hour', legend=False)
    plt.title('Top 10 Average Peak Energy Usage Hours/Days')
    plt.xlabel('Average Energy Consumption (kWH)')
    plt.ylabel('Day and Hour')
    plt.tight_layout()
    plot6_path = os.path.join(output_dir, 'top_peak_usage.png')
    plt.savefig(plot6_path)
    plt.close()
    print(f"Saved plot to {plot6_path}")

    print("All plot generation complete. Check the 'plots' directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate various plots from Duke Energy CSV data.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-i', '--input',
        type=str,
        default='Energy_Usage_Detailed.csv',
        help='Path to the input CSV file generated by xml_to_csv_formatter.py.\nDefault: Energy_Usage_Detailed.csv'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='plots',
        help='Directory for the output plot images. Will be created if it does not exist.\nDefault: plots'
    )

    args = parser.parse_args()

    generate_energy_usage_plots(args.input, args.output)