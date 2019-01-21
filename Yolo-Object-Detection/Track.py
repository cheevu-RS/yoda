import time
import cv2
import math
import numpy as np
import pprint
from darkflow.net.build import TFNet

#Assinging the model paths
options = {"model": "cfg/tiny-yolo.cfg", "load": "bin/tiny-yolo.weights", "threshold": 0.3}
tfnet = TFNet(options)

#Video paths
file_path = "./Sample-Videos/test6.mp4"
#file_path = 0
camera = cv2.VideoCapture(file_path)

#Testing the speed
count = 0
t = time.time()

#Tracking object label
object_label = "car"
distance_threshold = 300
size_inc_fac = 1.4
size_dec_fac = 0.6
max_thickness = 10
initialized = False
object_parameters = dict()

#Helper function to assing target label
def assignTargetLabel(predictions, object_label):
    same_class = list()
    for prediction in predictions:
        if prediction["label"] == object_label:
            same_class.append(prediction)
    max_conf = 0
    prediction_ret = None
    for prediction in same_class:
        if prediction["confidence"] > max_conf:
            max_conf = prediction["confidence"]
            prediction_ret = prediction
    if prediction_ret is not None:
        return prediction_ret, True
    else:
        return prediction_ret, False

#Helper function to find distance between 2 points
def dist(point1, point2):
    dist1 = (point1["x"] - point2["x"]) * (point1["x"] - point2["x"])
    dist2 = (point1["y"] - point2["y"]) * (point1["y"] - point2["y"])
    dist  = math.sqrt(dist1 + dist2)
    return dist

#Helper function to find centoid given top left and bottom right coordinates
def findCentroid(topLeft, bottomRight):
    centroid = dict()
    centroid["x"] = (topLeft["x"] + bottomRight["x"]) / 2
    centroid["y"] = (topLeft["y"] + bottomRight["y"]) / 2
    return centroid

#Getting change in size of object
def sizeChange(topLeft1, bottomRight1, topLeft2, bottomRight2):
    width1 = bottomRight1["x"] - topLeft1["x"]
    height1 = bottomRight1["y"] - topLeft1["y"]
    area1  = width1 * height1
    width2 = bottomRight2["x"] - topLeft2["x"]
    height2 = bottomRight2["y"] - topLeft2["y"]
    area2  = width2 * height2
    return float(area2) / float(area1)

#Helper function to find same object
def findObject(predictions, object_label): 
    #Finding all the predictions in the given class
    same_objects = list()
    for prediction in predictions:
        if prediction["label"] == object_label:
            same_objects.append(prediction)
    
    #If the class dosen't exist, change initialized to none
    if len(same_objects) == 0:
        initialized = False
        return None

    #Finding the object closest to the previous position of the object
    min_dist = 10000
    target_object = dict()
    
    #Finding the centroid of the target object
    target_centroid = findCentroid(object_parameters["topleft"], object_parameters["bottomright"])
    for object_new in same_objects:
        #Finding the centroid of new bounding box
        box_centroid = findCentroid(object_new["topleft"], object_new["bottomright"])
        dist_new = dist(target_centroid, box_centroid) 
            
        if dist_new < min_dist:
            min_dist = dist_new
            target_object = object_new
        
    #Finding the size change of the target object
    size_ratio = sizeChange(object_parameters["topleft"], object_parameters["bottomright"], target_object["topleft"], target_object["bottomright"])

    #Check if the new target passes the scale test and distance test
    if min_dist < distance_threshold and (size_ratio < size_inc_fac and size_ratio > size_dec_fac):
        #print("Tracking")
        return target_object
    else:
        print("Your min dist is ", min_dist)
        print("The threshold values are ", distance_threshold, " and ", size_dec_fac, " and ", size_inc_fac)
        print("Not tracking")
        return target_object

#Reading video frames
while camera.isOpened():
    count += 1
    _, frame = camera.read()
    
    predictions = tfnet.return_predict(frame)
    #print(predictions)

    #If the target label hasn't been spotted, assign the target label
    if not initialized:
        object_parameters, initialized = assignTargetLabel(predictions, object_label)
    else:
        #Looking for the target object in the frame
        output_preds = findObject(predictions, object_label)
        if output_preds is not None:
            cv2.rectangle(frame, (output_preds["topleft"]["x"], output_preds["topleft"]["y"]), (output_preds["bottomright"]["x"], output_preds["bottomright"]["y"]), (255, 255, 255), int(max_thickness * output_preds["confidence"]))
            cv2.putText(frame, output_preds["label"], (int((output_preds["topleft"]["x"] + output_preds["bottomright"]["x"]) / 2), output_preds["topleft"]["y"]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
            object_parameters = output_preds
            #pprint.pprint(object_parameters)
            
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if count == 1:
            break

print("Average time: ", (time.time() - t) / count)
camera.release()
cv2.destroyAllWindows()
