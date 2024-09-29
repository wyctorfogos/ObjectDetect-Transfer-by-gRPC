import grpc
from concurrent import futures
import cv2
import base64
from utils import video_pb2
from utils import video_pb2_grpc

# Implementando o serviço de transmissão de vídeo
class VideoStreamServicer(video_pb2_grpc.VideoStreamServicer):
    def StreamFrame(self, request, context):
        # Aqui você poderia implementar algo como armazenar o frame recebido
        print(f"Frame recebido de tamanho {len(request.frame)}")
        return video_pb2.FrameResponse(status="Frame recebido com sucesso")

# Iniciar o servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    video_pb2_grpc.add_VideoStreamServicer_to_server(VideoStreamServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado na porta 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
