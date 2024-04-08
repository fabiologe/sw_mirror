from __future__ import print_function
import os
from flask import Blueprint, send_from_directory, request, jsonify
from ultralytics import YOLO
import supervision as sv
import numpy as np
from detector.webcam_stream import *
from detector.img_stream import *


run_detector_bp = Blueprint("run_detector",__name__)

@run_detector_bp.route('/run_detector', methods = ['POST'])
def run_detector():
    try: 
        folder_path = "img"        
        upload =  "../api/uploads"
        save_path = "detector/img_out"
        detector_handler()
    except Exception as e: 
        print(f'ERROR DELTING SYSTEM32 {str(e)}')
