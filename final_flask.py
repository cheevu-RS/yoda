import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
import json
import base64
import os
import pprint
import time
import cv2
from darkflow.net.build import TFNet

app = Flask(__name__)
socket = SocketIO(app, logger=True, engineio_logger=True)

options = {"model": "cfg/tiny-yolo.cfg", "load": "bin/tiny-yolo.weights", "threshold": 0.3}
tfnet = TFNet(options)
image = 'l'
result ='l'

@socket.on('connect')
def send_image():
    global image
    global result
    # print (image,result)
    socket.emit('send_image',  dict(image=image,result=result))

def listen():
    cap = cv2.VideoCapture(0)
    print (cap.isOpened())
    while True:
        # Capture frame-by-frame
        ret, imgcv = cap.read()
        # cv2.imshow('image',imgcv)
        cur_time = time.time()
        result1 = tfnet.return_predict(imgcv)
        # print("Time elapsed:" , (time.time() - cur_time ))
        # encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
        # res, encimg=cv2.imencode('.jpg',imgcv,encode_param)
        cv2.imwrite('img_CV2_90.jpg', imgcv, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        file1 = open('img_CV2_90.jpg','rb').read()

        global image
        global result
        image = base64.b64encode(file1)
        result = str(result1)
        send_image()
        eventlet.sleep(0)
        
eventlet.spawn(listen)

if __name__ == '__main__':
    socket.run(app, host='127.0.0.1')