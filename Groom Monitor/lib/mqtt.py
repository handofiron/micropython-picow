from umqtt.simple import MQTTClient
from secrets import CLIENT_ID, MQTT_SERVER, MQTT_USERNAME, MQTT_PASSWORD, DEBUG_MODE

# Function to print debug messages
def debug_print(message):
    if DEBUG_MODE:
        print('[DEBUG-MQTT]', message)

def on_message(topic, message):
    debug_print('Received message:')
    debug_print('Topic: {}'.format(topic))
    debug_print('Message: {}'.format(message.decode()))

def connect_to_mqtt():
    client = MQTTClient(client_id=CLIENT_ID, server=MQTT_SERVER, user=MQTT_USERNAME, password=MQTT_PASSWORD, keepalive=3600)
    client.DEBUG = DEBUG_MODE  # Enable or disable MQTT library debug output
    client.set_callback(on_message)

    debug_print('Connecting to {} MQTT Broker...'.format(MQTT_SERVER))
    client.connect()
    debug_print('Connected to {} MQTT Broker'.format(MQTT_SERVER))

    debug_print('Subscribing to topics...')
    client.subscribe(b'/GreenRoom/')
    client.subscribe(b'sensor/data')
    # Add more topic subscriptions as needed

    return client
