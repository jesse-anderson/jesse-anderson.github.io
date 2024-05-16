import Adafruit_DHT
import requests
import time
from datetime import datetime

# Sensor setup
SENSOR = Adafruit_DHT.DHT11  # Using DHT11 sensor
PIN = 4  # Change this to the GPIO pin number that the sensor is connected to

# Buffer to store data
data_buffer = []

while True:
    # Read humidity and temperature from DHT sensor
    humidityPercent, temperature_C = Adafruit_DHT.read_retry(SENSOR, PIN)
    
    if humidityPercent is not None and temperature_C is not None:
        
        # Prepare the data payload
        temperature_F = temperature_C * 9.0 / 5.0 + 32
        now = datetime.now()
        date = now.strftime("%m-%d-%Y")
        timeNow = now.strftime("%H:%M:%S")
        
        data = {
            'date': date,
            'time': timeNow,
            'humidityPercent': humidityPercent,
            'temperatureFahrenheit': temperature_F,
            'temperatureCelsius': temperature_C
        }
        # Log data to buffer
        data_buffer.append(data)
        print(f"Logged data: {data}")
        #clear data buffer
        data_buffer.clear()
    # Wait for 1 second before logging the next reading
    time.sleep(1)
