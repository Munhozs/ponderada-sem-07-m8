import network
import time
from machine import Pin, I2C 
from simple import MQTTClient
import bme280  

i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=400000)
bme = bme280.BME280(i2c=i2c)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("BETANIA_2G","37215623Casa")
time.sleep(5)
print(wlan.isconnected())

mqtt_server = 'mqtt-dashboard.com'
client_id = 'judBtcUGGL'
topic_temperature = b'Temperatura'
topic_pression = b'Pressao'
topic_humidity = b'Umidade'



def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(10)
    #machine.reset()
    client.connect()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
    

while True:
    try:
        print(bme.values[0])
        print(bme.values[1])
        print(bme.values[2])
        
        client.publish(topic_temperature, str(bme.values[0]))
        time.sleep(3)
        client.publish(topic_pression, str(bme.values[1]))
        time.sleep(3)
        client.publish(topic_humidity, str(bme.values[2]))
        time.sleep(3)
        
    except OSError as e:
        print("Error:", e)
        reconnect()