import librosa
from paho.mqtt import client as mqtt_client
from scipy.io.wavfile import write
import json
import time

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic = "projeto_aaib"
topic1 = "som"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client()       
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


    
def publish(client):
    y, sr = librosa.load('grav1.wav') 
    yy = y.tolist()
    df = json.dumps(yy)
    msg = df
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Message sent to topic `{topic1}`")
    else:
        print(f"Failed to send message to topic {topic1}")

        
def subscribe(client: mqtt_client):
    def on_message(client, userdata, start):
        print(f"Received start from `{start.topic}` topic")
        inicio = (start.payload.decode('utf-8'))
        if inicio == 'start':
            publish(client)

    client.subscribe(topic)
    client.on_message = on_message
        
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()