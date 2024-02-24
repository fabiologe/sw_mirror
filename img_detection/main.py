'''import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
from detector.webcam_stream import *
from detector.img_stream import *'''
from out.post import post_img, post_ez
import argparse

def main():
        folder_path = "img"        
        upload =  "../api/uploads"
        save_path = "detector/img_out"
        '''detector_handler()'''
        post_ez(folder_path, upload)

if __name__ == "__main__":
    main()
