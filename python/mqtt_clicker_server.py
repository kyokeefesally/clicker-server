#!/usr/bin/env python

import time
import multiprocessing

# Import package
import paho.mqtt.client as mqtt

from status_worker import StatusPoller as status_poller

# Define Variables
MQTT_BROKER = "localhost"
#MQTT_BROKER = "broker.shiftr.io"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_CLIENT_ID = "clicker_server"
MQTT_TOPIC = 'ww/response'

CUR_VALUE = None

'''
def mqtt_client_connect(MQTT_TOPIC):
    # Define on_connect event Handler
    def on_connect(mosq, obj, rc):
        #Subscribe to a the Topic
        mqttc.subscribe(MQTT_TOPIC, 0)

    # Define on_subscribe event Handler
    def on_subscribe(mosq, obj, mid, granted_qos):
        print "Subscribed to MQTT Topic"

    # Define on_message event Handler
    def on_message(mosq, obj, msg):
        global CUR_VALUE
        # get new_value from MQTT message
        new_value = msg.payload

        # check to see if value has changed
        if new_value != CUR_VALUE:
            print new_value
            # update stored current value
            CUR_VALUE = new_value

        #print msg.payload
        

    # Initiate MQTT Client
    mqttc = mqtt.Client(client_id=MQTT_CLIENT_ID)

    # Register Event Handlers
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe

    # Uncomment to connect to Broker w/auth mqttc.username_pw_set('username', 'password')
    #mqttc.username_pw_set('5e8cd9c3', '87bfb9a8dbdd4038')

    # Connect with MQTT Broker
    mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL )

    # Continue the network loop
    mqttc.loop_forever()
'''



def main():
    mqtt_client_connect(MQTT_TOPIC)


if __name__ == "__main__":
    _thread = status_poller()
    _thread.daemon = True
    _thread.start()
    main()