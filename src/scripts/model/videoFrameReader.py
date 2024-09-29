import os
import cv2
import time
import base64
from ultralytics import YOLO
import grpc
from . import video_pb2
from . import video_pb2_grpc

# Conectar ao servidor gRPC
channel = grpc.insecure_channel('localhost:50051')
stub = video_pb2_grpc.VideoStreamStub(channel)

# Carregar o modelo YOLO
model = YOLO("./weights/yolov8s.pt")
# Obter os nomes das classes
classNames = model.names

def readAndDetectObjects(videoPath):
    # Abrir o vídeo
    cap = cv2.VideoCapture(videoPath)

    while cap.isOpened():
        ret, frame = cap.read()
        
        if ret:
            # Fazer a predição
            results = model.predict(frame)
            
            # Para cada resultado (detecção), desenhar a caixa e a probabilidade
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Extrair coordenadas da caixa e a probabilidade
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas da caixa delimitadora
                    confidence = box.conf[0]  # Probabilidade de detecção
                    class_id = int(box.cls[0])  # Classe detectada (opcional, dependendo do modelo)
                    
                    # Desenhar a caixa delimitadora no frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Colocar o texto da probabilidade acima da caixa
                    Label = f'Label: {classNames[class_id]}'
                    cv2.putText(frame, Label, (x1-10, y1-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    confLabel = f'Conf: {confidence:.2f}'
                    cv2.putText(frame, confLabel, (x1-10, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            # Codificar o frame para base64
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Enviar o frame via gRPC
            response = stub.StreamFrame(video_pb2.FrameRequest(frame=frame_base64))
            print(f"Resposta do servidor: {response.status}")
            
            # Pressionar 'q' para sair
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    # Quando tudo terminar, liberar os recursos
    cap.release()
    cv2.destroyAllWindows()