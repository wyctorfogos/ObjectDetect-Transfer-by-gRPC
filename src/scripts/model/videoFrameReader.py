import os
import cv2
import time
from ultralytics import YOLO

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

            
            # Exibir o frame com as detecções
            cv2.imshow('Frame', frame)
            
            # Pressionar 'q' para sair
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    # Quando tudo terminar, liberar os recursos
    cap.release()
    cv2.destroyAllWindows()