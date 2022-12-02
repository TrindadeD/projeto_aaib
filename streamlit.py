import streamlit as st
#import pandas as pd
import numpy as np
from paho.mqtt import client as mqtt_client

st.title('Extração de Features de um ficheiro áudio')

#################### GRAVAR E GUARDAR FICHEIRO DE SOM #########################

import sounddevice as sd
from scipy.io.wavfile import write

########################### GRAVAR AUDIO ######################################

if st.button('Gravar Áudio'):
    
    broker = 'mqtt.eclipseprojects.io'
    port = 1883
    topic = "projeto_aaib"
    
    def connect_mqtt():
        def on_connect (client, userdata, flags, rc):
            if rc==0:
                st.print('connected')
            else:
                st.print("Failed to connect, return code %d\n", rc)
        client=mqtt_client.Client()
        client.on_connect = on_connect
        client.connect(broker, port)
        return client
    
    def publish(client):
        som=('a')
        result = client.publish(topic, som)
        status = result[0]
        if status == 0:
            print(f"som")
        else:
            print(f"Failed to send message to topic {topic}")
    def run():
        client = connect_mqtt()
        client.loop_start()
        publish(client)
        client.loop_stop()

    if __name__ == '__main__':
        run()