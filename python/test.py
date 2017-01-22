#!/usr/bin/env python

import time
from threading import Thread
from flask import Flask, render_template, session, request, redirect, Response
from flask_socketio import SocketIO, emit
import eventlet
import paho.mqtt.client as mqtt
import os
import subprocess
import signal
import sys

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

mqtt_thread = None


## =================================================
class MQTT_Thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stop = False
        
    def run(self):
        while not self.stop and mqttc.loop() == 0:
            pass
            
        #print "MQTT Thread Closed"
# ==================================================

def signal_handler(signal, frame):
    mqtt_thread.stop = True
    #print('==== Ctrl+C EXIT ====')
    sys.exit(0)

def on_message(mosq, obj, msg):
    socketio.emit('my_response',{'topic':msg.topic,'payload':msg.payload}) 
    print(msg.payload)
    
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

# Start MQTT
mqttc = mqtt.Client(client_id='clicker_server')
mqttc.on_message = on_message
mqttc.connect("localhost", 1883, 60)
mqttc.subscribe("ww/response", 0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    '''
    status_thread = status_poller()
    status_thread.daemon = True
    status_thread.start()
    '''

    mqtt_thread = MQTT_Thread()
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=extra_files, port=3000)
