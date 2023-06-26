import machine
from secrets import DEBUG_MODE

# Function to print debug messages
def debug_print(message):
    if DEBUG_MODE:
        print('[DEBUG-Water Level Sensor]', message)

# Function to check the water level sensor status
def check_water_level_sensor():
    # Configure pin 7 as an input
    sensor_pin = machine.Pin(4, machine.Pin.IN)

    # Check the water level sensor status
    if sensor_pin.value():
        debug_print('Water level sensor is Wet.')
        status = 'Wet'
    else:
        debug_print('Water level sensor is Dry.')
        status = 'Dry'

    return status
