#!/usr/bin/env python

import time
import multiprocessing

import paho.mqtt.client as mqtt

# Define Variables
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_CLIENT_ID = "status_worker"
MQTT_TOPIC = "ww/command"
MQTT_MSG = "ka 00 00"


class StatusPoller(multiprocessing.Process):
 
    def __init__(self):
        multiprocessing.Process.__init__(self)

        # Initiate MQTT Client
        self.mqttc = mqtt.Client(client_id=MQTT_CLIENT_ID)

        # Register Event Handlers
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish

        # Connect with MQTT Broker
        self.mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL )


    # Define on_connect event Handler
    def on_connect(self, mosq, obj, rc):
        #print "Connected to MQTT Broker"
        pass

    # Define on_publish event Handler
    def on_publish(self, client, userdata, mid):
        #print "Message Published..."
        pass

    def mqtt_publish(self, topic, payload):
        self.mqttc.publish(topic, payload)

    def get_power_status(self):
        self.mqtt_publish(MQTT_TOPIC, 'ka 00 ff')


    def run(self):
        while True:
            self.get_power_status()
            time.sleep(2)


def main():
    _thread = StatusPoller()
    _thread.start()

if __name__ == '__main__':
    main()



