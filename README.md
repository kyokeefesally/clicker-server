# clicker-server
MQTT / SocketIO server for clicker TV controllers

## WORK IN PROGRESS

## RPi Setup Steps
Install requirements:
```bash
sudo apt-get update
sudo apt-get -y install python-pip
sudo pip install paho-mqtt
sudo pip install Flask
sudo pip install flask-socketio

sudo apt-get -y install build-essential libssl-dev libffi-dev python-dev
sudo apt-get -y install libevent-dev
sudo apt-get -y install python-all-dev

sudo apt-get -y install libnss-mdns

sudo pip install eventlet

sudo apt-get install nodejs npm node-semver

```
## Setting up MQTT Broker - Installing Mosquitto on to a RPi
SSH into Raspberry Pi and create a new directory for temp files –
```bash
mkdir mosquitto
cd mosquitto
```
Import the repository package signing key –
```bash
wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
sudo apt-key add mosquitto-repo.gpg.key
```
Make the repository available to apt –
```bash
cd /etc/apt/sources.list.d/
sudo wget http://repo.mosquitto.org/debian/mosquitto-jessie.list
```
Install Mosquitto MQTT Broker –
```bash
sudo apt-get install mosquitto
```
Check Mosquitto Service Status, Process and Default Port (1883) –
```bash
service mosquitto status
ps -ef | grep mosq
netstat -tln | grep 1883
```