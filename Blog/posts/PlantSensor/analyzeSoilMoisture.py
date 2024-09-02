import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

# Define the file path to the CSV file
csv_file = 'Plant_Sensor - Sheet1.csv' # not using a gui for once. one off plotting to assess soil moisture trends to set arbitrary buzzer.

# Define the expected column names
column_names = ['Date', 'Time', 'Temp', 'Humidity', 'Lux', 'CCT', 'Soil Moisture', 'Soil Temp', 'R', 'G', 'B', 'HTML']

# Load the CSV file into a DataFrame, reading everything as strings initially for later processing.
df = pd.read_csv(csv_file, header=0, names=column_names, dtype=str, low_memory=False)

# Clean up the data by removing any spaces within numeric fields and converting to appropriate types
for column in ['Temp', 'Humidity', 'Lux', 'CCT', 'Soil Moisture', 'Soil Temp', 'R', 'G', 'B']:
    df[column] = df[column].str.replace(' ', '', regex=False)  # Remove spaces
    df[column] = pd.to_numeric(df[column], errors='coerce')    # Convert to numeric, set invalid parsing as NaN

# Convert 'Date' and 'Time' columns into a single datetime column with explicit format, this was major hiccup.
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Drop any rows where 'Datetime' could not be parsed, data cleaning general
df.dropna(subset=['Datetime'], inplace=True)

# Set 'Datetime' column as index
df.set_index('Datetime', inplace=True)

# Define columns
columns_of_interest = ['Temp', 'Lux', 'CCT', 'Soil Moisture', 'Soil Temp']

# Process data in parallel, but plot sequentially in main thread
def prepare_data(column):
    if column in df.columns:
        return df.index, df[column]
    else:
        print(f"Warning: '{column}' column not found in the data.")
        return None, None

# Use ThreadPoolExecutor to parallelize the data prep
with ThreadPoolExecutor() as executor:
    results = list(executor.map(prepare_data, columns_of_interest))

# Plotting in the main thread
for i, (time_index, data_series) in enumerate(results):
    if time_index is not None:
        plt.figure(figsize=(7, 4))
        plt.plot(time_index, data_series, label=columns_of_interest[i])
        plt.title(f'{columns_of_interest[i]} over Time')
        plt.xlabel('Time')
        plt.ylabel(columns_of_interest[i])
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()