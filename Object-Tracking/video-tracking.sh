source ~/OpenCV/bin/activate
python track_object.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel --label person --output output/raceTracked.mp4 --video ./input/race.mp4
