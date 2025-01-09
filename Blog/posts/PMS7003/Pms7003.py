import machine
import struct
import time

class UartError(Exception):
    """Custom exception for UART errors."""
    pass

class PMS7003:
    START_BYTE_1 = 0x42
    START_BYTE_2 = 0x4D
    FRAME_LENGTH = 32
    STABILIZATION_TIME = 30
    SLEEP_TIME = 30 #change me to 270 for simpler control. Will put into sleep mode for 270 sec.

    # GPIO pin assignments
    SET_PIN = 22
    RESET_PIN = 14

    def __init__(self, uart=2, mode='verbose', passive=False):
        """Initialize UART and set the mode."""
        self.uart = machine.UART(uart, baudrate=9600, bits=8, parity=None, stop=1)
        self.mode = mode.lower()
        self.passive = passive
        self.is_enabled = True
        self.is_sleeping = False
        if self.passive:
            self._enter_passive_mode()
        else:
            self._enter_active_mode()

    def enable_sensor(self):
        """Enable the sensor by setting the SET pin."""
        self.set_pin = machine.Pin(PMS7003.SET_PIN, machine.Pin.OUT)
        self.set_pin.value(1)
        self.is_enabled = True
        self.wakeup()

    def disable_sensor(self):
        """Disable the sensor by clearing the SET pin."""
        self.set_pin = machine.Pin(PMS7003.SET_PIN, machine.Pin.OUT)
        self.set_pin.value(0)
        self.is_enabled = False
        self.clear_uart_buffer()  # Clear any residual data in the buffer
        #self.sleep()

    def reset_sensor(self):
        """Reset the sensor by toggling the RESET pin."""
        self.reset_pin = machine.Pin(PMS7003.RESET_PIN, machine.Pin.OUT)
        self.reset_pin.value(0)
        time.sleep(0.1)  # Hold reset low for 100ms
        self.reset_pin.value(1)
        time.sleep(self.STABILIZATION_TIME)
        if self.passive:
            self._enter_passive_mode()
        else:
            self._enter_active_mode()

    def sleep(self):
        """Put the sensor into sleep mode."""
        command = bytearray([PMS7003.START_BYTE_1, PMS7003.START_BYTE_2, 0xE4, 0x00])
        checksum = sum(command)
        command.append((checksum >> 8) & 0xFF)  # High byte of checksum
        command.append(checksum & 0xFF)         # Low byte of checksum
        self.clear_uart_buffer()  # Clear UART buffer before sending the command
        self.send_command(command) #I guess this turns the laser off
        time.sleep(1) #give machine time to process???
        self.send_command(bytearray([PMS7003.START_BYTE_1, PMS7003.START_BYTE_2, 0xE4, 0x00, 0x00, 0x01, 0x73])) #Fan off
        self.is_sleeping = True
        print("Sensor is now in sleep mode (fan and laser should be off).")
        
    def clear_uart_buffer(self):
        """Clear any remaining data in the UART buffer."""
        while self.uart.any():
            self.uart.read()  # Read and discard any remaining data

    def wakeup(self):
        """Wake the sensor up from sleep mode."""
        command = bytearray([PMS7003.START_BYTE_1, PMS7003.START_BYTE_2, 0xE4, 0x01])
        checksum = sum(command)
        command.append((checksum >> 8) & 0xFF)  # High byte of checksum
        command.append(checksum & 0xFF)         # Low byte of checksum
        self.clear_uart_buffer()  # Clear UART buffer before sending the command
        self.send_command(command) #I guess this turns the laser back on
        time.sleep(1) #give machine time to process???
        self.send_command(bytearray([PMS7003.START_BYTE_1, PMS7003.START_BYTE_2, 0xE4, 0x00, 0x01, 0x01, 0x74])) #Fan on
        self.is_sleeping = False
        time.sleep(self.STABILIZATION_TIME)  # Allow sensor to stabilize after waking
        print("Sensor is now awake (fan and laser should be on).")
        
        if self.passive:
            self._enter_passive_mode()
        else:
            self._enter_active_mode()

    def send_command(self, cmd):
        """Send a command to the sensor."""
        checksum = sum(cmd)
        cmd.append((checksum >> 8) & 0xFF)
        cmd.append(checksum & 0xFF)
        self.uart.write(cmd)

    def _enter_passive_mode(self):
        cmd = bytearray([PMS7003.START_BYTE_1, PMS7003.START_BYTE_2, 0xE1, 0x00, 0x00, 0x01, 0x70])
        self.send_command(cmd)

    def _enter_active_mode(self):
        cmd = bytearray([PMS7003.START_BYTE_1, PMS7003.START_BYTE_2, 0xE1, 0x00, 0x01, 0x01, 0x71])
        self.send_command(cmd)

    def _request_data_passive(self):
        cmd = bytearray([PMS7003.START_BYTE_1, PMS7003.START_BYTE_2, 0xE2, 0x00, 0x00, 0x01, 0x71])
        self.send_command(cmd)

    def read_data(self):
        """Read and parse a data frame from the sensor."""
        if self.passive:
            self._request_data_passive()
        max_attempts = 5  # Maximum number of attempts to read valid data
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            first_byte = self.uart.read(1)
            if first_byte is None or first_byte[0] != self.START_BYTE_1:
                continue

            second_byte = self.uart.read(1)
            if second_byte is None or second_byte[0] != self.START_BYTE_2:
                continue

            read_bytes = self.uart.read(self.FRAME_LENGTH - 2)
            if len(read_bytes) < self.FRAME_LENGTH - 2:
                continue

            # Unpack the data
            data = struct.unpack('>HHHHHHHHHHHHHBB', read_bytes)

            # Validate checksum
            checksum = self.START_BYTE_1 + self.START_BYTE_2 + sum(read_bytes[:-2])
            received_checksum = (read_bytes[-2] << 8) + read_bytes[-1]
            if checksum != received_checksum:
                continue

            # Return based on the selected mode
            if self.mode == 'factory':
                return {
                    'PM1.0_CF1': data[0],
                    'PM2.5_CF1': data[1],
                    'PM10_CF1': data[2]
                }
            elif self.mode == 'atmospheric':
                return {
                    'PM1.0_ATM': data[3],
                    'PM2.5_ATM': data[4],
                    'PM10_ATM': data[5]
                }
            elif self.mode == 'particle':
                return {
                    'Particles_0.3um': data[6],
                    'Particles_0.5um': data[7],
                    'Particles_1.0um': data[8],
                    'Particles_2.5um': data[9],
                    'Particles_5.0um': data[10],
                    'Particles_10.0um': data[11]
                }
            elif self.mode == 'verbose':
                return {
                    'PM1.0_CF1': data[0],
                    'PM2.5_CF1': data[1],
                    'PM10_CF1': data[2],
                    'PM1.0_ATM': data[3],
                    'PM2.5_ATM': data[4],
                    'PM10_ATM': data[5],
                    'Particles_0.3um': data[6],
                    'Particles_0.5um': data[7],
                    'Particles_1.0um': data[8],
                    'Particles_2.5um': data[9],
                    'Particles_5.0um': data[10],
                    'Particles_10.0um': data[11]
                }
        print("Max attempts reached for data acquisition. Returning None.")
        return None
    def check_state(self):
        """Return the current state of the sensor."""
        state_info = {
            'UART': self.uart,
            'Mode': self.mode,
            'Passive': self.passive,
            'Enabled': self.is_enabled,
            'Sleeping': self.is_sleeping
        }
        return state_info
