import machine
import onewire
import ds18x20
import secrets
from secrets import DEBUG_MODE
import time

# Function to print debug messages
def debug_print(message):
    if DEBUG_MODE:
        print('[DEBUG-DS18x20]', message)

# GPIO Pin connected to the DS18B20 sensors
ds_pin = machine.Pin(7)

# Create a OneWire bus
ds_bus = onewire.OneWire(ds_pin)

# Create a DS18X20 sensor object
ds_sensor = ds18x20.DS18X20(ds_bus)

# Define the sensor addresses
SENSOR_2_ADDRESS = bytearray([0x28, 0x41, 0x1B, 0x81, 0xE3, 0xE1, 0x3C, 0x89])
SENSOR_1_ADDRESS = bytearray([0x28, 0xB4, 0xDB, 0x81, 0xE3, 0xE1, 0x3C, 0x32])

# Function to read the temperatures from both sensors
def measure_temperatures():
    # Main code for temperature measurement
    while True:
        ds_sensor.convert_temp()
        time.sleep_ms(750)  # Wait for the temperature conversion to complete
    
        temperatures = []
        temperature_sensor1 = ds_sensor.read_temp(SENSOR_1_ADDRESS)
        temperatures.append(temperature_sensor1)
        debug_print("Water Tank Temp: {:.2f}°C".format(temperature_sensor1))

        temperature_sensor2 = ds_sensor.read_temp(SENSOR_2_ADDRESS)
        temperatures.append(temperature_sensor2)
        debug_print("Room Temp: {:.2f}°C".format(temperature_sensor2))

        # Assign temperature_2 for use in main.py
        global temperature_2
        temperature_2 = temperature_sensor2
    
        return temperatures, temperature_2
