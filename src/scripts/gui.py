import streamlit as st
import grpc
import cv2
import base64
import numpy as np
import time
from utils import video_pb2, video_pb2_grpc  # Certifique-se de ter o código gerado pelo gRPC

# Definindo a interface do Streamlit
st.title("Visualização do Stream de Vídeo")

# Configurar canal gRPC e stub
channel = grpc.insecure_channel('localhost:50051')  # Endereço do seu servidor gRPC
stub = video_pb2_grpc.VideoStreamStub(channel)

# Placeholder para os frames do vídeo
frame_placeholder = st.empty()
start_stream = st.checkbox("Iniciar Stream")

if start_stream:
    while True:
        try:
            # Solicitar frame ao servidor gRPC
            response = stub.StreamFrame(video_pb2.FrameRequest())
            decoded_frame = base64.b64decode(response.frame)
            np_arr = np.frombuffer(decoded_frame, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is not None:
                # Reduzir a resolução do frame para melhorar a performance
                resized_frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
                # Converter a imagem para RGB
                rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                # Exibir o frame no Streamlit
                frame_placeholder.image(rgb_frame, channels="RGB")
            else:
                st.warning("Erro ao decodificar o frame")

            # Intervalo para evitar sobrecarga na página
            time.sleep(0.1)

        except Exception as e:
            st.error(f"Erro ao receber o frame: {str(e)}")
            break