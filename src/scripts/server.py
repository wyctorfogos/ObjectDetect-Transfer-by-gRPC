import grpc
from concurrent import futures
import cv2
import base64
import numpy as np
from utils import video_pb2
from utils import video_pb2_grpc

# Implementando o serviço de transmissão de vídeo
class VideoStreamServicer(video_pb2_grpc.VideoStreamServicer):
    def StreamFrame(self, request, context):
        # Recebendo o frame em base64
        print(f"Frame recebido de tamanho {len(request.frame)}")
        
        try:
            # Decodificar o frame de base64 para bytes
            decoded_frame = base64.b64decode(request.frame)
            
            # Converter os bytes para uma matriz NumPy
            np_arr = np.frombuffer(decoded_frame, np.uint8)
            
            # Decodificar a imagem a partir dos bytes em um frame utilizável pelo OpenCV
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if frame is not None:
                # Exibir o frame decodificado
                print(f"Dimensões do frame: {frame.shape}")
                cv2.imshow("Frame decodificado", frame)
                cv2.waitKey(1)  # Pequeno atraso para permitir a exibição dos frames
            else:
                print("Erro: não foi possível decodificar o frame.")
        
        except Exception as e:
            print(f"Erro durante a decodificação do frame: {str(e)}")
        
        
        return video_pb2.FrameResponse(status="Frame recebido com sucesso")

# Iniciar o servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    video_pb2_grpc.add_VideoStreamServicer_to_server(VideoStreamServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado na porta 50051...")
    cv2.destroyAllWindows()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
