from Pms7003 import PMS7003
import time

def test_sensor_modes_and_passive():
    """Test every combination of mode and passive state, with resets in between."""
    print("\nTEST SENSOR MODES AND PASSIVE STATES\n")
    modes = ['factory', 'atmospheric', 'particle', 'verbose']
    passive_states = [False, True]

    # Loop through all combinations of modes and passive states
    for mode in modes:
        for passive in passive_states:
            print(f"\nTesting mode: {mode}, Passive: {passive}")

            # Initialize the sensor
            sensor = PMS7003(uart=2, mode=mode, passive=passive)
            print(sensor.check_state())
            # Reset the sensor
            sensor.reset_sensor()
            print(f"Sensor has been reset. Mode: {mode}, Passive: {passive}")
            
            # Allow the sensor to warm up
            time.sleep(30)  # Warming up the sensor
            
            # Take 3 readings
            for i in range(3):
                time.sleep(5)
                print(f"\nSensor Mode: {sensor.mode}")
                print(f"Passive Mode: {sensor.passive}")
                print(f"Reading: {i + 1}")
                data = sensor.read_data()

                if data is not None:
                    # Print data based on the selected mode
                    if sensor.mode in ['factory', 'verbose']:
                        print(f"PM1.0_CF1: {data.get('PM1.0_CF1')}")
                        print(f"PM2.5_CF1: {data.get('PM2.5_CF1')}")
                        print(f"PM10_CF1: {data.get('PM10_CF1')}")
                    
                    if sensor.mode in ['atmospheric', 'verbose']:
                        print(f"PM1.0_ATM: {data.get('PM1.0_ATM')}")
                        print(f"PM2.5_ATM: {data.get('PM2.5_ATM')}")
                        print(f"PM10_ATM: {data.get('PM10_ATM')}")

                    if sensor.mode in ['particle', 'verbose']:
                        print(f"Particles_0.3um: {data.get('Particles_0.3um')}")
                        print(f"Particles_0.5um: {data.get('Particles_0.5um')}")
                        print(f"Particles_1.0um: {data.get('Particles_1.0um')}")
                        print(f"Particles_2.5um: {data.get('Particles_2.5um')}")
                        print(f"Particles_5.0um: {data.get('Particles_5.0um')}")
                        print(f"Particles_10.0um: {data.get('Particles_10.0um')}")
                else:
                    print("Failed to retrieve valid data.")

    print("\nTesting complete.\n")

# Call the function to start the test
# test_sensor_modes_and_passive()

def test_enable_disable_sensor():
    """Test enabling and disabling the sensor."""
    print("\nTEST ENABLING AND DISABLING SENSOR\n")
    # Initialize the sensor (using default mode and passive state)
    sensor = PMS7003(uart=2, mode='verbose', passive=False)
    
    # Warm up the sensor initially
    print("Warming up the sensor...")
    time.sleep(30) #change to 30

    # Take a reading with the sensor enabled
    print("\nSensor enabled. Taking 3 readings:")
    sensor.enable_sensor()  # Enable the sensor
    print(sensor.check_state())
    for i in range(3):
        time.sleep(5)
        print(f"\nReading {i + 1} (Sensor enabled):")
        data = sensor.read_data()
        print(sensor.check_state())
        if data is not None:
                    # Print data based on the selected mode
                    if sensor.mode in ['factory', 'verbose']:
                        print(f"PM1.0_CF1: {data.get('PM1.0_CF1')}")
                        print(f"PM2.5_CF1: {data.get('PM2.5_CF1')}")
                        print(f"PM10_CF1: {data.get('PM10_CF1')}")
                    
                    if sensor.mode in ['atmospheric', 'verbose']:
                        print(f"PM1.0_ATM: {data.get('PM1.0_ATM')}")
                        print(f"PM2.5_ATM: {data.get('PM2.5_ATM')}")
                        print(f"PM10_ATM: {data.get('PM10_ATM')}")

                    if sensor.mode in ['particle', 'verbose']:
                        print(f"Particles_0.3um: {data.get('Particles_0.3um')}")
                        print(f"Particles_0.5um: {data.get('Particles_0.5um')}")
                        print(f"Particles_1.0um: {data.get('Particles_1.0um')}")
                        print(f"Particles_2.5um: {data.get('Particles_2.5um')}")
                        print(f"Particles_5.0um: {data.get('Particles_5.0um')}")
                        print(f"Particles_10.0um: {data.get('Particles_10.0um')}")
        else:
                    print("Failed to retrieve valid data.")

    # Disable the sensor
    print("\nDisabling the sensor...")
    sensor.disable_sensor()
    print(sensor.check_state())
    time.sleep(5)

    # Try to read data when the sensor is disabled
    print("\nAttempting to read data while the sensor is disabled (no readings should be received):")
    data = sensor.read_data()
    print(data)
    if data is None:
        print("No data received, as expected (sensor is disabled).")

    # Re-enable the sensor and take another set of readings
    print("\nRe-enabling the sensor and taking 3 more readings:")
    sensor.enable_sensor()  # Re-enable the sensor
    print(sensor.check_state())
    for i in range(3):
        time.sleep(30)
        print(f"\nReading {i + 1} (Sensor re-enabled):")
        data = sensor.read_data()
        if data is not None:
                    # Print data based on the selected mode
                    if sensor.mode in ['factory', 'verbose']:
                        print(f"PM1.0_CF1: {data.get('PM1.0_CF1')}")
                        print(f"PM2.5_CF1: {data.get('PM2.5_CF1')}")
                        print(f"PM10_CF1: {data.get('PM10_CF1')}")
                    
                    if sensor.mode in ['atmospheric', 'verbose']:
                        print(f"PM1.0_ATM: {data.get('PM1.0_ATM')}")
                        print(f"PM2.5_ATM: {data.get('PM2.5_ATM')}")
                        print(f"PM10_ATM: {data.get('PM10_ATM')}")

                    if sensor.mode in ['particle', 'verbose']:
                        print(f"Particles_0.3um: {data.get('Particles_0.3um')}")
                        print(f"Particles_0.5um: {data.get('Particles_0.5um')}")
                        print(f"Particles_1.0um: {data.get('Particles_1.0um')}")
                        print(f"Particles_2.5um: {data.get('Particles_2.5um')}")
                        print(f"Particles_5.0um: {data.get('Particles_5.0um')}")
                        print(f"Particles_10.0um: {data.get('Particles_10.0um')}")
        else:
                    print("Failed to retrieve valid data.")
    
    print("\nEnable/Disable sensor test complete.")

# Call the function to test enable/disable functionality
# test_enable_disable_sensor()

def test_sleep_wakeup():
    """Test the sleep and wakeup functions of the sensor."""
    print("\n TEST SLEEP AND WAKE FUNCTIONALITY\n")
    # Initialize the sensor within the function
    sensor = PMS7003(uart=2, mode='verbose', passive=False)

    # Take an initial reading to ensure the sensor is working
    print("Taking initial readings before sleep:")
    for i in range(3):
        time.sleep(5)
        data = sensor.read_data()
        if data:
            if sensor.mode in ['factory', 'verbose']:
                print(f"PM1.0_CF1: {data.get('PM1.0_CF1')}, PM2.5_CF1: {data.get('PM2.5_CF1')}, PM10_CF1: {data.get('PM10_CF1')}")
            
            if sensor.mode in ['atmospheric', 'verbose']:
                print(f"PM1.0_ATM: {data.get('PM1.0_ATM')}, PM2.5_ATM: {data.get('PM2.5_ATM')}, PM10_ATM: {data.get('PM10_ATM')}")
            
            if sensor.mode in ['particle', 'verbose']:
                print(f"Particles_0.3um: {data.get('Particles_0.3um')}, Particles_0.5um: {data.get('Particles_0.5um')}, Particles_1.0um: {data.get('Particles_1.0um')}, Particles_2.5um: {data.get('Particles_2.5um')}, Particles_5.0um: {data.get('Particles_5.0um')}, Particles_10.0um: {data.get('Particles_10.0um')}")
        else:
            print("Failed to retrieve valid data.")

    # Put the sensor to sleep
    print("\nPutting the sensor to sleep...")
    sensor.sleep()
    time.sleep(5)
    # Check state after sleep
    state = sensor.check_state()
    print("\nSensor state after sleep:")
    for key, value in state.items():
        print(f"{key}: {value}")

    # Attempt to read data while the sensor is asleep (over 1 minute)
    print("\nAttempting to read data while the sensor is asleep for 1 minute:")
    #Note that this turns the fan off! It can still read but the fan is otherwise off.
    #This will preserve the fan, but not the laser I guess.
    for i in range(6):  # Try every 10 seconds over 1 minute
        time.sleep(10)
        data = sensor.read_data()
        if data:
            print(f"Reading {i + 1} while asleep: {data}")
        else:
            print(f"Reading {i + 1} while asleep: No data (sensor is asleep).")

    # Wake the sensor up
    print("\nWaking up the sensor...")
    sensor.wakeup()
    # Check state after wakeup
    state = sensor.check_state()
    print("\nSensor state after wakeup:")
    for key, value in state.items():
        print(f"{key}: {value}")
    
    # Take another set of readings after wakeup
    print("\nTaking readings after wakeup:")
    for i in range(3):
        time.sleep(5)
        data = sensor.read_data()
        if data:
            if sensor.mode in ['factory', 'verbose']:
                print(f"PM1.0_CF1: {data.get('PM1.0_CF1')}, PM2.5_CF1: {data.get('PM2.5_CF1')}, PM10_CF1: {data.get('PM10_CF1')}")
            
            if sensor.mode in ['atmospheric', 'verbose']:
                print(f"PM1.0_ATM: {data.get('PM1.0_ATM')}, PM2.5_ATM: {data.get('PM2.5_ATM')}, PM10_ATM: {data.get('PM10_ATM')}")
            
            if sensor.mode in ['particle', 'verbose']:
                print(f"Particles_0.3um: {data.get('Particles_0.3um')}, Particles_0.5um: {data.get('Particles_0.5um')}, Particles_1.0um: {data.get('Particles_1.0um')}, Particles_2.5um: {data.get('Particles_2.5um')}, Particles_5.0um: {data.get('Particles_5.0um')}, Particles_10.0um: {data.get('Particles_10.0um')}")
        else:
            print("Failed to retrieve valid data.")
    
    print("\nSleep/Wakeup test complete.")

# Call the function to test sleep and wakeup functionality
# test_sleep_wakeup()

def continuous_readings(sensor=PMS7003(uart=2, mode='verbose', passive=False), interval=30):
    """Continuously read sensor data at a given interval (in seconds)."""
    #Higher sampling frequency seems to lead to more dropped measurements.
    # It seems to drop a certain amount after a given time after startup
    #Maybe best to speed through the first 100 or s
    print("\nTEST CONTINUOUS READINGS\n")
    # Start the sensor and loop indefinitely
    print("Starting continuous readings...")
    while True:
        try:
            time.sleep(interval)  # Wait for the specified interval
            data = sensor.read_data()  # Read the sensor data

            if data:
                # Print the data based on the mode
                if sensor.mode in ['factory', 'verbose']:
                    print(f"PM1.0_CF1: {data.get('PM1.0_CF1')}, PM2.5_CF1: {data.get('PM2.5_CF1')}, PM10_CF1: {data.get('PM10_CF1')}\n")
                
                if sensor.mode in ['atmospheric', 'verbose']:
                    print(f"PM1.0_ATM: {data.get('PM1.0_ATM')}, PM2.5_ATM: {data.get('PM2.5_ATM')}, PM10_ATM: {data.get('PM10_ATM')}\n")
                
                if sensor.mode in ['particle', 'verbose']:
                    print(f"Particles_0.3um: {data.get('Particles_0.3um')}, Particles_0.5um: {data.get('Particles_0.5um')}, Particles_1.0um: {data.get('Particles_1.0um')}, Particles_2.5um: {data.get('Particles_2.5um')}, Particles_5.0um: {data.get('Particles_5.0um')}, Particles_10.0um: {data.get('Particles_10.0um')}\n")
            else:
                print("Failed to retrieve valid data.")

        except KeyboardInterrupt:
            print("\nContinuous readings stopped.")
            break  # Exit the loop when interrupted
        
# continuous_readings()

def intermittent_reading(sensor=PMS7003(uart=2, mode='verbose', passive=False), interval=240):
    """
    Take readings every 'interval' seconds (default is 5 minutes).
    The sensor turns on, waits 30 seconds to stabilize, takes readings for 1 minute (2 readings), and then powers off.
    """
    print("Starting intermittent readings...")
    
    while True:
        count = 0
        fails = 0
        try:
            # Turn on the sensor and wake it up
            print("\nTurning on sensor...")
            sensor.enable_sensor() #wwe wake up within this and we also take some time to stabilzie here so no need for extra code
            
            # Take readings for 1 minute (2 readings every 30 seconds)
            #change loop to count to 2 successful tries then reset!!!!!
            while True:
                print(f"Taking reading {count + 1}...")
                data = sensor.read_data()
                time.sleep(30)
                if data:
                    count = count +1
                    # Print the data based on the mode
                    if sensor.mode in ['factory', 'verbose']:
                        print(f"PM1.0_CF1: {data.get('PM1.0_CF1')}, PM2.5_CF1: {data.get('PM2.5_CF1')}, PM10_CF1: {data.get('PM10_CF1')}")
                    
                    if sensor.mode in ['atmospheric', 'verbose']:
                        print(f"PM1.0_ATM: {data.get('PM1.0_ATM')}, PM2.5_ATM: {data.get('PM2.5_ATM')}, PM10_ATM: {data.get('PM10_ATM')}")
                    
                    if sensor.mode in ['particle', 'verbose']:
                        print(f"Particles_0.3um: {data.get('Particles_0.3um')}, Particles_0.5um: {data.get('Particles_0.5um')}, Particles_1.0um: {data.get('Particles_1.0um')}, Particles_2.5um: {data.get('Particles_2.5um')}, Particles_5.0um: {data.get('Particles_5.0um')}, Particles_10.0um: {data.get('Particles_10.0um')}")
                    if count == 2:
                        print("2 data records acquired. Sleepy time.")
                        break
                else:
                    print("Failed to retrieve valid data. Attempting again...")
                    fails = fails +1
                    if fails == 3:
                        print("3 failed reads. Resetting...")
                        break

            # Power off the sensor
            print("Powering off the sensor...")
            sensor.sleep()
            sensor.disable_sensor()

            # Wait for the next cycle
            print(f"Waiting {interval / 60} minutes for the next set of readings...")
            time.sleep(interval)

        except KeyboardInterrupt:
            print("\nIntermittent readings stopped.")
            break  # Exit the loop when interrupted

# Example usage:
intermittent_reading(interval=300)  # Every 5 minutes (300 seconds)