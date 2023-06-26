from machine import ADC
import secrets
from secrets import DEBUG_MODE

tds_sensor = ADC(27)  # TDS Sensor
aref = 3.3

ec = -0.11
tds = 0
ecCalibration = 1

# Modify these calibration and conversion factors according to your sensors
tds_calibration_factor = 1.75
ec_conversion_factor = 1.3

# Function to print debug messages
def debug_print(message):
    if DEBUG_MODE:
        print('[DEBUG-TDS Sensor]', message)

def convert_voltage_to_tds(voltage, temperature):
    temperature_coefficient = 1.0 + 0.02 * (temperature - 25.0)
    ec = (voltage / temperature_coefficient) * ecCalibration
    tds = (133.42 * ec**3 - 255.86 * ec**2 + 857.39 * ec) * 0.5 * tds_calibration_factor
    return tds

def convert_voltage_to_ec(voltage, temperature):
    temperature_coefficient = 1.0 + 0.02 * (temperature - 25.0)
    ec = (voltage / temperature_coefficient) * ecCalibration * ec_conversion_factor
    return ec

# Update the function signature to accept temperature_sensor2 as a parameter
def measure_tds(temperature_sensor2):
    raw_ec = tds_sensor.read_u16() * aref / 65535.0  # Read the analog value
    tds = convert_voltage_to_tds(raw_ec, temperature_sensor2)
    ec = convert_voltage_to_ec(raw_ec, temperature_sensor2)
    debug_print("TDS: {:.2f}".format(tds))
    debug_print("EC: {:.2f}".format(ec))
    debug_print("Temperature: {:.2f}".format(temperature_sensor2))

    return tds, ec
