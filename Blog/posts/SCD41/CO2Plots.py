import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Function to open a file dialog and let the user select a CSV file
def choose_file():
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(filetypes=[("CSV files", "*.csv")])
    return filename

# Load the CSV file into a DataFrame
file_path = choose_file()
if not file_path:
    print("No file selected.")
else:
    df = pd.read_csv(file_path)

    # Convert 'Date' and 'Time' columns into a single datetime column
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%Y %H:%M:%S')

    # Set the 'Datetime' column as the index
    df.set_index('Datetime', inplace=True)

    # Plot CO2 levels over time
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['CO2'], label='CO2 (ppm)')
    plt.title('CO2 Levels Over Time')
    plt.xlabel('Time')
    plt.ylabel('CO2 (ppm)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Plot Temperature and Humidity over time
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Temperature'], label='Temperature (°F)', color='red')
    plt.plot(df.index, df['Humidity'], label='Humidity (%)', color='blue')
    plt.title('Temperature and Humidity Over Time')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°F) / Humidity (%)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
