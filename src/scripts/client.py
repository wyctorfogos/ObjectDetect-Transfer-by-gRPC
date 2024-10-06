import logging
import os
import cv2
import time
import time
from model.videoFrameReader import readAndDetectObjects
import socket

if __name__=="__main__":
    videoPath="videos/No Copyright Videos People Walking _ Free Stock Background.mp4"

    while True:
        try:
            readAndDetectObjects(videoPath)
        except Exception as e:
            logging.exception("Erro ao tentar analizar o vídeo: {e}\n")
        finally:
            logging.info("Tentativa de envio finalizada!\n")

        time.sleep(10) # Tentativa de conexão a cada 10 segundos