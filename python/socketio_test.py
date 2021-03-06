#!/usr/bin/env python

import time
import multiprocessing

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet

import paho.mqtt.client as mqtt

from status_worker import StatusPoller as status_poller

# Start with a basic flask app
app = Flask(__name__)

# Flask configs
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# Extra files to monitor for reloader
extra_files = ['static/js/app.js', 'templates/index.html',]

#turn the flask app into a socketio app
socketio = SocketIO(app, debug=True)

# MQTT Variables
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_CLIENT_ID = "clicker_server"
MQTT_TOPIC = 'ww/response'

CUR_VALUE = None
mqtt_thread = None


## =================================================
'''
class MQTT_Thread(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        # Initiate MQTT Client
        self.mqttc = mqtt.Client(client_id='clicker_server')

        
        

    def run(self):
        # Define on_connect event Handler
        def on_connect(mosq, obj, rc):
            #Subscribe to a the Topic
            self.mqttc.subscribe('ww/response', 0)

        # Define on_subscribe event Handler
        def on_subscribe(mosq, obj, mid, granted_qos):
            print "Subscribed to MQTT Topic"

        # Define on_message event Handler
        def on_message(mosq, obj, msg):
            socketio.emit('my_response',{'data': 'thread started'},broadcast=True)
            global CUR_VALUE
            # get new_value from MQTT message
            new_value = msg.payload

            # check to see if value has changed
            if new_value != CUR_VALUE:
                print new_value
                # update stored current value
                CUR_VALUE = new_value

            #print msg.payload

        # Register Event Handlers
        self.mqttc.on_message = on_message
        self.mqttc.on_connect = on_connect
        self.mqttc.on_subscribe = on_subscribe

        # Uncomment to connect to Broker w/auth mqttc.username_pw_set('username', 'password')
        #mqttc.username_pw_set('5e8cd9c3', '87bfb9a8dbdd4038')

        # Connect with MQTT Broker
        self.mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL )

        # Continue the network loop
        self.mqttc.loop_forever()
'''       

class MqttProcess(multiprocessing.Process):
 
    def __init__(self):
        multiprocessing.Process.__init__(self)


    def run(self):
        # Define on_connect event Handler
        def on_connect(mosq, obj, rc):
            #Subscribe to a the Topic
            self.mqttc.subscribe('ww/response', 0)

        # Define on_subscribe event Handler
        def on_subscribe(mosq, obj, mid, granted_qos):
            print("Subscribed to MQTT Topic")

        # Define on_message event Handler
        def on_message(mosq, obj, msg):
            print("message received")
            


        # Initiate MQTT Client
        self.mqttc = mqtt.Client(client_id='clicker_server')

        # Register Event Handlers
        self.mqttc.on_message = on_message
        self.mqttc.on_connect = on_connect
        self.mqttc.on_subscribe = on_subscribe

        # Uncomment to connect to Broker w/auth mqttc.username_pw_set('username', 'password')
        #mqttc.username_pw_set('5e8cd9c3', '87bfb9a8dbdd4038')

        # Connect with MQTT Broker
        #self.mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL )
        self.mqttc.connect('localhost', 1883, 45)

        # Continue the network loop
        self.mqttc.loop_forever()

# ==================================================


#---------------Flask-SocketIO--------------#

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('my_response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('web_message')
def handle_message(message):
    print('received message: ' + str(message))

#---------------END Flask-SocketIO--------------#

#----------------MQTT---------------#

'''
#def mqtt_client_connect(MQTT_TOPIC):

# Define on_connect event Handler
def on_connect(mosq, obj, rc):
    #Subscribe to a the Topic
    mqttc.subscribe(MQTT_TOPIC, 0)

# Define on_subscribe event Handler
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed to MQTT Topic")

# Define on_message event Handler
def on_message(mosq, obj, msg):
    print("new mqtt message to clicker_server: " + msg.payload)
    socketio.emit('my_response',{'topic':msg.topic,'payload':msg.payload},broadcast=True)
    print("message should have been emitted")


# Initiate MQTT Client
mqttc = mqtt.Client(client_id=MQTT_CLIENT_ID)

# Register Event Handlers
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Uncomment to connect to Broker w/auth mqttc.username_pw_set('username', 'password')
#mqttc.username_pw_set('5e8cd9c3', '87bfb9a8dbdd4038')

# Connect with MQTT Broker
print("before connect")
mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL )
print("after connect")

# Continue the network loop
#mqttc.loop_forever()
'''

#-------------END MQTT---------------#

if __name__ == '__main__':
    status_thread = status_poller()
    status_thread.daemon = True
    status_thread.start()
    '''
    mqtt_thread = MqttProcess()
    mqtt_thread.daemon = True
    mqtt_thread.start()
    '''

    socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=extra_files, port=3000)
