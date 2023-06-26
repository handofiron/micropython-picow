import time
import utime
import ujson
from machine import Pin, Timer, WDT
from wifi import connect_to_wifi
from mqtt import connect_to_mqtt
from secrets import DEBUG_MODE
from ds18b20 import measure_temperatures
from water_level_sensor import check_water_level_sensor

led = Pin("LED", Pin.OUT)
timer = Timer()
wdt = WDT(timeout=8388)  # Set the watchdog timeout to 5 seconds (5000 milliseconds)

# Function to print debug messages
def debug_print(message):
    if DEBUG_MODE:
        print('[DEBUG-Main]', message)

def blink(timer):
    led.toggle()

# Function to publish data to MQTT
def publish_data(topic, data):
    mqtt_client.publish(topic, ujson.dumps(data))

# Main program
if __name__ == "__main__":
    if DEBUG_MODE:
        print("Debug mode enabled!")

    wdt.feed()  # Reset the watchdog timer

    # Connect to Wi-Fi
    connect_to_wifi()
    wdt.feed()  # Reset the watchdog timer

    # Connect to MQTT
    mqtt_client = connect_to_mqtt()
    wdt.feed()  # Reset the watchdog timer

    # Main loop
    while True:
        wdt.feed()  # Reset the watchdog timer

        timer.init(freq=6.0, mode=Timer.PERIODIC, callback=blink)

        # Check water level sensor
        water_level_status = check_water_level_sensor()
        debug_print("Water Level Sensor Status: " + water_level_status)

        # Measure temperatures from DS18B20 sensors
        temperatures = measure_temperatures()

        # Measure TDS value
        from ds18b20 import temperature_2 # Update import statement
        from tds_sensor import measure_tds
        # Update the following line to use temperature_2 instead of water_temp
        tds_value, ec_value = measure_tds(temperature_sensor2=temperatures[1])

        # Create a dictionary with the measured data
        data = {
            "water_level": water_level_status,
            "temperature_1": temperatures[0],
            "temperature_2": temperature_2,  # Use temperature_2 from ds18b20.py
            "tds_value": tds_value,
            "ec_value": ec_value,
            "timestamp": time.time()
        }

        # Publish data to MQTT
        publish_data("sensor/data", data)

        # Delay for a certain period of time (e.g., 5 seconds)
        time.sleep(5)
        wdt.feed()

