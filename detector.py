# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import cv2
import dlib

#Creating the arguement parset
argpar = argparse.ArgumentParser() 
argpar.add_argument("-s", "--shape-predictor", required = True, help = "Path to pre-trained model for face recognition features")
argpar.add_argument("-a", "--alarm", type = str, default = "./alarm.mp3", help = "Path to alarm sound file")
argpar.add_argument("-w", "--webcam", type = int, default = 0, help = "Index of the webcam")
args = vars(argpar.parse_args())
print(args)

#Defining the constants necessary for finding eye aspect ratio
eye_ratio_thresh = 0.3
closed_length = 48
alarm_on = False
counter = 0

#Creating helper function to play sound
def sound_alarm(path):
    # play an alarm sound
    playsound.playsound(path)

#Creating helper function to find if eye is closed or open
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    aspect_ratio = (A + B) / (2 * C)

    return aspect_ratio

#Loading the face detector based on HOG 
print("Loading the detector")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

print("Working till here")

#Getting the indexes for relavent facial landmarks for left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

print("Starting video camera")
vs = VideoStream(src = args["webcam"]).start()
time.sleep(1.0)

while True:
    frame = vs.read()
    
    #Resizing to the correct format
    frame = imutils.resize(frame, width = 450)
    
    #Gray scaling
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detecting faces
    rects = detector(gray, 0)

    #Iterating through the detected faces
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        
        leftEye = shape[lStart: lEnd]
        rightEye = shape[rStart: rEnd]

        leftEar = eye_aspect_ratio(leftEye)
        rightEar = eye_aspect_ratio(rightEye)
        
        #Average eye aspect ratio
        ear = (leftEar + rightEar) / 2.0

        #Visualise the contours of the eye
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (255, 0, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (255, 0, 0), 1)

        #Check for drowsiness
        if ear < eye_ratio_thresh:
            counter += 1

            #If eyes are consecutively closed for a large amount of time
            if counter > closed_length: 
                if not alarm_on:
                    alarm_on = True
                #If an alarm sound file is given
                if args["alarm"] != "":
                    t = Thread(target = sound_alarm, args = args["alarm"],)
                    t.daemon = True
                    t.start()

                #Draw an alarm on the frame
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            COUNTER = 0
            ALARM_ON = False
        
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    #Show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    #If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
