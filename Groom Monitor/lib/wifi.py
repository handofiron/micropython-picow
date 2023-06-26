import network
import secrets
from machine import Pin, Timer
from secrets import DEBUG_MODE

led = Pin("LED", Pin.OUT)
timer = Timer()

# Function to print debug messages
def debug_print(message):
    if DEBUG_MODE:
        print('[DEBUG-Wifi]', message)

def blink(timer):
    led.toggle()

def connect_to_wifi():
    wifi = network.WLAN(network.STA_IF)
    timer.init(freq=1.5, mode=Timer.PERIODIC, callback=blink)
    wifi.active(True)

    if wifi.isconnected():
        debug_print("Already connected to Wi-Fi")
        return

    debug_print("Scanning for Wi-Fi networks...")
    available_networks = wifi.scan()

    debug_print("Found {} Wi-Fi networks".format(len(available_networks)))

    for network_info in available_networks:
        ssid = network_info[0].decode()
        debug_print("Found network: {}".format(ssid))
        for network_name, network_credentials in secrets.WIFI_NETWORKS.items():
            if ssid.lower() == network_credentials["ssid"].lower():
                debug_print("Connecting to Wi-Fi network: {}".format(ssid))
                wifi.connect(network_credentials["ssid"], network_credentials["password"])
                while not wifi.isconnected():
                    pass
                debug_print("Wi-Fi connected!")
                debug_print("IP address: {}".format(wifi.ifconfig()[0]))
                return

    debug_print("No configured Wi-Fi network found")
