import cv2
import argparse

from ultralytics import YOLO
import supervision as sv
import numpy as np
from detector.webcam_stream import detector
person_inside = False
#cropping image : 
'''detection = sv.Detections(...)
with sv.ImageSink(target_dir_path='target/directory/path') as sink:
    for xyxy in detection.xyxy:
        cropped_image = sv.crop_image(image=image, xyxy=xyxy)
        sink.save_image(image=image)'''







def main():
    detector()


if __name__ == "__main__":
    main()
