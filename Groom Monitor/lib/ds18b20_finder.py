import machine
import onewire
import ds18x20
import time

# GPIO Pin connected to the DS18B20 sensors
ds_pin = machine.Pin(7)

# Create a OneWire bus
ds_bus = onewire.OneWire(ds_pin)

# Create a DS18X20 sensor object
ds_sensor = ds18x20.DS18X20(ds_bus)

# Function to scan the OneWire bus and retrieve sensor addresses
def scan_sensor_addresses():
    roms = ds_sensor.scan()
    addresses = []
    for rom in roms:
        address = "bytearray(["
        for i, byte in enumerate(rom):
            address += "0x{:02x}".format(byte)
            if i != len(rom) - 1:
                address += ", "
        address += "])"
        addresses.append(address)
    return addresses

# Function to read the temperatures from the sensors
def measure_temperatures():
    addresses = scan_sensor_addresses()
    if len(addresses) < 2:
        print("Error: Insufficient number of sensors detected.")
        return None
    
    # Main code for temperature measurement
    while True:
        ds_sensor.convert_temp()
        time.sleep_ms(750)  # Wait for the temperature conversion to complete
    
        temperatures = []
        for i, address in enumerate(addresses):
            rom = eval(address)
            temperature = ds_sensor.read_temp(rom)
            temperatures.append(temperature)
            print("SENSOR_{}_ADDRESS = {}".format(i+1, address))
            print("Temperature {}: {:.2f}°C".format(i+1, temperature))
        
        return temperatures

measure_temperatures()
