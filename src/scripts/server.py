import grpc
from concurrent import futures
import cv2
import base64
import numpy as np
import asyncio
import websockets
import webbrowser
import os
from utils import video_pb2
from utils import video_pb2_grpc

# Implementando o serviço de transmissão de vídeo
class VideoStreamServicer(video_pb2_grpc.VideoStreamServicer):
    def __init__(self):
        self.websocket_clients = set()

    async def notify_clients(self, frame):
        if self.websocket_clients:
            try:
                _, buffer = cv2.imencode('.jpg', frame)
                frame_jpg = base64.b64encode(buffer).decode('utf-8')
                await asyncio.wait([client.send(frame_jpg) for client in self.websocket_clients])
            except Exception as e:
                print(f"Erro ao enviar frame via WebSocket: {e}")

    def StreamFrame(self, request, context):        
        try:
            # Decodificar o frame de base64 para bytes
            decoded_frame = base64.b64decode(request.frame)
            
            # Converter os bytes para uma matriz NumPy
            np_arr = np.frombuffer(decoded_frame, np.uint8)
            
            # Decodificar a imagem a partir dos bytes em um frame utilizável pelo OpenCV
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if frame is not None:
                cv2.waitKey(1)  # Pequeno atraso para permitir a exibição dos frames
                # Notificar clientes WebSocket
                asyncio.run(self.notify_clients(frame))
            else:
                print("Erro: não foi possível decodificar o frame.")
        
        except Exception as e:
            print(f"Erro durante a decodificação do frame: {str(e)}")
        
        return video_pb2.FrameResponse(status="Frame recebido com sucesso")

# Iniciar o servidor gRPC e WebSocket
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    video_stream_servicer = VideoStreamServicer()
    video_pb2_grpc.add_VideoStreamServicer_to_server(video_stream_servicer, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado na porta 50051...")

    # Abrir a página web automaticamente
    web_page_path = os.path.abspath("src/scripts/view/index.html")
    webbrowser.open(f"file://{web_page_path}")

    async def websocket_handler(websocket, path):
        print("Novo cliente WebSocket conectado")
        video_stream_servicer.websocket_clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            video_stream_servicer.websocket_clients.remove(websocket)
            print("Cliente WebSocket desconectado")

    start_server = websockets.serve(websocket_handler, "0.0.0.0", 6789)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()

if __name__ == '__main__':
    serve()