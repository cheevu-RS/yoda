# import the necessary packages
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import dlib
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,	help="path to Caffe pre-trained model")
ap.add_argument("-v", "--video", default=0,	help="path to input video file")
ap.add_argument("-l", "--label", required=True,	help="class label we are interested in detecting + tracking")
ap.add_argument("-o", "--output", type=str,	help="path to optional output video file")
ap.add_argument("-c", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# load our serialized model from disk
print("Loading the model")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

#Initialzing the video stream
print("Reading the video")
vs = cv2.VideoCapture(args["video"])
tracker = None
writer = None
label = ""

#Keeping track of FPS
fps = FPS().start()

# loop over frames from the video file stream
while True:
	# grab the next frame from the video file
	(grabbed, frame) = vs.read()

	#Checking for end of video
	if frame is None:
		break

	#Resizing the frame
	frame = imutils.resize(frame, width=600)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# Initilizing the writer to write video to the disk
	if args["output"] is not None and writer is None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
			(frame.shape[1], frame.shape[0]), True)

	# If our correlation tracker has nothing to track, we need our object detector to find an object to track first
	if tracker is None:
		#Convert frame to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(frame, 0.007843, (w, h), 127.5)

		# Pass the blob through the network and obtain the detections and predictions
		net.setInput(blob)
		detections = net.forward()

		#Checking if atleast one prediction in the required class is made
		if len(detections) > 0:
			#Finding prediction with max confidence
			i = np.argmax(detections[0, 0, :, 2])

			#Getting the confidence score of the detections
			conf = detections[0, 0, i, 2]
			label = CLASSES[int(detections[0, 0, i, 1])]

			#Filtering detections with less confidence
			if conf > args["confidence"] and label == args["label"]:
				# Computing bounding boxes of objects
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				#Starts the correlation tracker
				tracker = dlib.correlation_tracker()
				rect = dlib.rectangle(startX, startY, endX, endY)
				tracker.start_track(rgb, rect)

				# Draw the bounding box and text for the object
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(0, 255, 0), 2)
				cv2.putText(frame, label, (startX, startY - 15),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

	#Object of required class detected
	else:
		# Update the tracker
		tracker.update(rgb)
		pos = tracker.get_position()

		# unpack the position object
		startX = int(pos.left())
		startY = int(pos.top())
		endX = int(pos.right())
		endY = int(pos.bottom())

		# draw the bounding box from the correlation object tracker
		cv2.rectangle(frame, (startX, startY), (endX, endY),
			(0, 255, 0), 2)
		cv2.putText(frame, label, (startX, startY - 15),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

	# check to see if we should write the frame to disk
	if writer is not None:
		writer.write(frame)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("The elapsed time is : {:.2f}".format(fps.elapsed()))
print("The approx. FPS is : {:.2f}".format(fps.fps()))

# check to see if we need to release the video writer pointer
if writer is not None:
	writer.release()

# do a bit of cleanup
cv2.destroyAllWindows()
vs.release()
