source ~/OpenCV/bin/activate
flow --model cfg/yolov2.cfg --load bin/yolov2.weights --demo ./Sample-Videos/test5.mp4 --gpu 1.0 --saveVideo
