import os
import cv2
import time
from model.videoFrameReader import readAndDetectObjects

if __name__=="__main__":
    videoPath="videos/No Copyright Videos People Walking _ Free Stock Background.mp4"
    try:
        readAndDetectObjects(videoPath)
    except Exception as e:
        print("Erro ao tentar analizar o vídeo: {e}\n")