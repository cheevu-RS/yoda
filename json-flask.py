from darkflow.net.build import TFNet
import cv2
import pprint
import os
import time
from darkflow.net.build import TFNet
import cv2

# from flask import Flask
# app = Flask(__name__)
# @app.route('/')
# def main():
options = {"model": "cfg/tiny-yolo.cfg", "load": "bin/tiny-yolo.weights", "threshold": 0.3}
tfnet = TFNet(options)
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, imgcv = cap.read()
    cur_time = time.time()
    result = tfnet.return_predict(imgcv)
    print("Time elapsed:" , (time.time() - cur_time ))
    # print (result)
    # return str(result)
    for i in range(len(result)):
        # if result[i]['confidence'] > 0.4:
        x1=result[i]['topleft']['x']
        y1=result[i]['topleft']['y']
        x2=result[i]['bottomright']['x']
        y2=result[i]['bottomright']['y']
        cv2.rectangle(imgcv, (x1, y1), (x2, y2), (255,0,0), 2)
        cv2.putText(imgcv, result[i]['label'], (int((x1+x2)/2),y1 ), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.imshow('image',imgcv)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# if __name__ == '__main__':
#     app.run(debug=True)