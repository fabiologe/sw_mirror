import cv2
import argparse
from ultralytics import YOLO
import supervision as sv
import numpy as np
from detector.webcam_stream import *
from detector.img_stream import *

def main():
        n_img = 1
        folder_path = "detector/img"
        save_path = "detector/img_out"
        detector_handler()


if __name__ == "__main__":
    main()
