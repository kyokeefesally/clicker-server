#!/usr/bin/env python

import time
import multiprocessing

# Import package
from flask import Flask, render_template, session, request, redirect, Response
from flask_socketio import SocketIO, emit
import socketio
from flask import jsonify
import eventlet

import paho.mqtt.client as mqtt

#from threading import Thread
import signal
import sys

from status_worker import StatusPoller as status_poller

# Define Variables
MQTT_BROKER = "localhost"
#MQTT_BROKER = "broker.shiftr.io"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_CLIENT_ID = "clicker_server"
MQTT_TOPIC = 'ww/response'

CUR_VALUE = None


# Start with a basic flask app
app = Flask(__name__)

# Flask configs
app.config['SECRET_KEY'] = 'secret!'
#app.secret_key = "secrettttt!"
app.config['DEBUG'] = True

# Extra files to monitor for reloader
extra_files = ['static/js/app.js', 'templates/index.html',]

#turn the flask app into a socketio app
socketio = SocketIO(app, debug=True)

mqtt_thread = None


## =================================================
'''
class MQTT_Thread(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop = False
        
    def run(self):
        while not self.stop and mqttc.loop_forever() == 0:
            pass
            
        #print "MQTT Thread Closed"
'''
# ==================================================

'''
def signal_handler(signal, frame):
    mqtt_thread.stop = True
    #print('==== Ctrl+C EXIT ====')
    sys.exit(0)
'''

@app.route('/')
def index():
    return "Hello, World!"

@socketio.on('connect')
def test_connect():
    socketio.emit('my response',{'topic':msg.topic,'payload':msg.payload})

@socketio.on('disconnect')
def test_disconnect():
    pass 


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
    socketio.emit('my response',{'topic':msg.topic,'payload':msg.payload})
    print


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



#signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    #mqtt_client_connect(MQTT_TOPIC)

    status_thread = status_poller()
    status_thread.daemon = True
    status_thread.start()
    '''
    mqtt_thread = MQTT_Thread()
    mqtt_thread.daemon = True
    mqtt_thread.start()
    '''


    socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=extra_files, port=3000)

