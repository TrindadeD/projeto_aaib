from paho.mqtt import client as mqtt_client
import streamlit as st
import librosa
import matplotlib.pyplot as plt
from librosa import display
import numpy as np

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic = "projeto_aaib" 

client = mqtt_client.Client()
client.connect(broker, port)
st.header('Extração de Features')
if st.button('Start'):
    def publish(client):
        inicio = 'start'
        result = client.publish(topic, inicio)
        status = result[0]
        if status == 0:
            print(f"Message sent to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    #st.title('Extração de Features de um ficheiro áudio')
    publish(client)
if st.button('Gráficos'):        
    #publish(client)

    st.header('Extração de Features')
    #y, sr = librosa.load('grav1.wav') #descarregar o ficheiro
    dados=np.loadtxt(r'C:\Users\ASUS\Desktop\MEB\2 ano\1 semestre\AAIB\projeto_alternativo\new_msg.csv', delimiter=',', dtype='str' )
    g = np.asarray(dados, dtype=np.float64)
    sr=22050
    # chromagram
    st.subheader('Chromagram')

    plt.figure(figsize=(15, 3))
    chromagram = librosa.feature.chroma_stft(g,sr=sr)
    librosa.display.specshow(chromagram)
    st.pyplot()
    
    
    # espetrograma
    st.subheader('Espectograma')
    
    X = librosa.stft(g)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(15, 3))
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    #mel spectograms
    st.subheader('Mel spectogram')
    
    plt.figure(figsize=(15, 3))
    s_audio = librosa.feature.melspectrogram(g, sr=sr)
    librosa.display.specshow(s_audio)
    st.pyplot()

    # Magnitude total do sinal (sonoridade / parametro de energia)
    st.subheader('Sonoridade')
    
    # Valor de RMS para cada valor de magnitude
    S, phase = librosa.magphase(librosa.stft(g)) #frequencia e fase
    rms = librosa.feature.rms(S=S) #root mean square da gravacao
    
    # Grafico
    fig, ax = plt.subplots(figsize=(15, 6), nrows=2, sharex=True)
    times = librosa.times_like(rms)
    ax[0].semilogy(times, rms[0], label='Energia RMS')
    ax[0].set(xticks=[])
    ax[0].legend()
    ax[0].label_outer()
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                            y_axis='log', x_axis='time', ax=ax[1])
    ax[1].set(title='Espetrograma da Magnitude logarítmico')
    st.pyplot()
    
    #zero crossing rate
    st.subheader('Zero Crossing Rate')
    
    zcrs = librosa.feature.zero_crossing_rate(g)
    print(f"Zero crossing rate: {sum(librosa.zero_crossings(g))}")
    plt.figure(figsize=(15, 3))
    plt.plot(zcrs[0])
    plt.title('Zero Crossing Rate')
    st.pyplot()