#!/usr/bin/env node

/**
 * Module dependencies.
 */

var express = require('express');

// create app, server, and io
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

// static routes
app.use(express.static('static'))

// global variables
var CUR_VAL = null

// routes
app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
  io.sockets.emit('my_response', CUR_VAL);
});


var mqtt = require('mqtt'), url = require('url');
// Parse 
var mqtt_url = url.parse(process.env.CLOUDMQTT_URL || 'mqtt://localhost:1883');
//var auth = (mqtt_url.auth || ':').split(':');
var url = "mqtt://" + mqtt_url.host;

var options = {
  port: mqtt_url.port,
  clientId: 'mqttjs_' + Math.random().toString(16).substr(2, 8),
  //username: auth[0],
  //password: auth[1],
};

// Create a client connection
var mqtt_client = mqtt.connect(url, options);

mqtt_client.on('connect', function() { // When connected
  console.log("mqtt client connected");

  // subscribe to a topic
  mqtt_client.subscribe('ww/response', function() {
    // when a message arrives, send it out to the websockets
    mqtt_client.on('message', function(topic, message, packet) {
      var new_value = message.toString()

      if (new_value != CUR_VAL) {
        console.log("Received '" + new_value + "' on '" + topic + "'");
        io.sockets.emit('my_response', new_value);
        CUR_VAL = new_value
      }
      
    });
  });
});

/*
mqtt_client.on('message', function (topic, message) {
  // message is Buffer 
  console.log(message.toString())
  client.end()
})
*/

// listen
http.listen(3000, function(){
  console.log('listening on *:3000');
});