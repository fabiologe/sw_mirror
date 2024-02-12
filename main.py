import cv2
import argparse
from ultralytics import YOLO
import supervision as sv
import numpy as np
from detector.webcam_stream import *
from detector.img_stream import *










def main():
        n_img = 4
        folder_path = "detector/img"
        save_path = "detector/img_out"
        detector_handler(path = folder_path, n_img= n_img)
        static_detector(folder_path , save_path)



if __name__ == "__main__":
    main()
