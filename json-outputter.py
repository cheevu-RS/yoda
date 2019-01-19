from darkflow.net.build import TFNet
import cv2
import pprint
import os
import time

from darkflow.net.build import TFNet
import cv2

options = {"model": "cfg/tiny-yolo.cfg", "load": "bin/tiny-yolo.weights", "threshold": 0.1}

tfnet = TFNet(options)

current_dir = os.getcwd()
img_dir  = '/sample_img/'
images = os.listdir(current_dir + img_dir)

cur_time = time.time()

for image in images:
    imgcv = cv2.imread("./sample_img/" + image)
    result = tfnet.return_predict(imgcv)
    #pprint.pprint(result)
    cv2.imshow('image', imgcv)
print("Time elapsed:" , (time.time() - cur_time ) / len(images))
